import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable in self.domains:
            removeables = set()

            # Check if each word in the variable's domain matches its length
            for word in self.domains[variable]:
                if len(word) != variable.length:
                    removeables.add(word)

            # Remove all marked words from the domain of the variable

            self.domains[variable] -= removeables

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        if self.crossword.overlaps[x, y] is None:
            return False

        i, j = self.crossword.overlaps[x, y]
        removeables = set()

        # Check for and record any conflicts
        for x_word in self.domains[x]:
            conflict = True
            for y_word in self.domains[y]:
                if x_word[i] == y_word[j]:
                    conflict = False

            if conflict:
                removeables.add(x_word)

        # If there are conflicts, remove them from x's domain
        if len(removeables) != 0:
            for word in removeables:
                self.domains[x].remove(word)
            return True

        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        queue = []
        if arcs == None:
            for arc in self.crossword.overlaps:
                queue.append(arc)
        else:
            queue = arcs

        while queue != []:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False

                neighbors = self.crossword.neighbors(x) - {y}
                for z in neighbors:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            elif assignment[variable] == None:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Ensure all words are distinct and have the correct length
        words = set()
        for var, word in assignment.items():
            # Check if the word length matches the variable's length
            if len(word) != var.length:
                return False
            # Check if the word is unique
            if word in words:
                return False
            words.add(word)

        for var1 in assignment:
            for var2 in self.crossword.neighbors(var1):

                if var2 not in assignment:
                    continue

                overlap = self.crossword.overlaps[var1, var2]
                if overlap != None:
                    i, j = overlap

                    if assignment[var1][i] != assignment[var2][j]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Create a list to store each value and the number of conflicts it causes
        conflicts = []

        # Iterate over each value in var's domain
        for value in self.domains[var]:
            num_conflicts = 0

            # Check each neighbor of var
            for neighbor in self.crossword.neighbors(var):
                # Only consider neighbors that are not already assigned
                if neighbor not in assignment:
                    # Find overlap between var and neighbor
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap != None:
                        i, j = overlap
                        # Count how many values in the neighbor's domain are inconsistent
                        for neighbor_value in self.domains[neighbor]:
                            if value[i] != neighbor_value[j]:
                                num_conflicts += 1

            # Add the value and number of conflicts it causes to the list
            conflicts.append((value, num_conflicts))

        # Sort conflicts list by the number of conflicts (smallest number of conflicts first)
        for i in range(len(conflicts)):
            for j in range(i + 1, len(conflicts)):
                if conflicts[i][1] > conflicts[j][1]:
                    # Swap the elements
                    temp = conflicts[i]
                    conflicts[i] = conflicts[j]
                    conflicts[j] = temp

        # Create a list of values sorted by the number of conflicts
        sorted_values = []
        for value, _ in conflicts:
            sorted_values.append(value)

        # Return the sorted list of values
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = []
        for variable in self.domains:
            if variable not in assignment:
                unassigned_vars.append(variable)

        if unassigned_vars == []:
            return None

        remaining = len(self.domains[unassigned_vars[0]])
        for var in unassigned_vars:
            length = len(self.domains[var])
            if length < remaining:
                remaining = length

        ranked = []
        for var in unassigned_vars:
            length = len(self.domains[var])
            if length == remaining:
                ranked.append(var)

        max = 0
        for var in ranked:
            length = len(self.crossword.neighbors(var))
            if length > max:
                max = length

        ranked = [var for var in ranked if len(self.crossword.neighbors(var)) == max]
        return ranked[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        domain_values = self.order_domain_values(var, assignment)
        for value in domain_values:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result != None:
                    return result

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
