"""Student Grade Calculator."""

FILE_NAME = "student_grades.txt"


def calculate_average(test1, test2, test3):
	"""Return the average of three test scores."""
	return (test1 + test2 + test3) / 3


def calculate_grade(average):
	"""Return a letter grade for an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def is_exit_command(value):
	"""Return True when the user requests program exit."""
	return value == "\x1b" or value.strip().upper() in {"ESC", "EXIT"}


def get_text(prompt):
	"""Prompt for required text, allowing the user to exit."""
	while True:
		value = input(prompt)
		if is_exit_command(value):
			return None
		value = value.strip()
		if value:
			if "|" in value:
				print("Please do not use the pipe character (|).")
			else:
				return value
		else:
			print("This field cannot be blank.")


def get_score(prompt):
	"""Prompt for a test score from 0 through 100."""
	while True:
		value = input(prompt)
		if is_exit_command(value):
			return None
		try:
			score = float(value)
		except ValueError:
			print("Please enter a number from 0 to 100.")
			continue
		if 0 <= score <= 100:
			return score
		print("Please enter a score from 0 to 100.")


def add_student(students):
	"""Prompt for and append one student record."""
	print("\nAdd Student (press ESC to cancel)")
	name = get_text("Student name: ")
	if name is None:
		print("Add student cancelled.")
		return
	student_id = get_text("Student ID: ")
	if student_id is None:
		print("Add student cancelled.")
		return
	test1 = get_score("Test 1 score: ")
	if test1 is None:
		print("Add student cancelled.")
		return
	test2 = get_score("Test 2 score: ")
	if test2 is None:
		print("Add student cancelled.")
		return
	test3 = get_score("Test 3 score: ")
	if test3 is None:
		print("Add student cancelled.")
		return

	average = calculate_average(test1, test2, test3)
	students.append({
		"name": name,
		"id": student_id,
		"test1": test1,
		"test2": test2,
		"test3": test3,
		"average": average,
		"grade": calculate_grade(average),
	})
	print(f"Added {name} with an average of {average:.2f} ({students[-1]['grade']}).")


def display_students(students):
	"""Display every student record in a formatted table."""
	if not students:
		print("\nNo student records found.")
		return

	headers = ["Name", "ID", "Test 1", "Test 2", "Test 3", "Average", "Grade"]
	rows = []
	for student in students:
		rows.append([
			student["name"],
			student["id"],
			f"{student['test1']:.2f}",
			f"{student['test2']:.2f}",
			f"{student['test3']:.2f}",
			f"{student['average']:.2f}",
			student["grade"],
		])
	widths = [max(len(header), *(len(row[index]) for row in rows))
			  for index, header in enumerate(headers)]
	separator = "-+-".join("-" * width for width in widths)

	print("\nStudent Records")
	print(" | ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
	print(separator)
	for row in rows:
		print(" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)))


def display_statistics(students):
	"""Display highest, lowest, and overall class averages."""
	if not students:
		print("\nNo student records available for statistics.")
		return
	averages = [student["average"] for student in students]
	highest = max(students, key=lambda student: student["average"])
	lowest = min(students, key=lambda student: student["average"])
	print("\nClass Statistics")
	print(f"Highest average: {highest['average']:.2f} ({highest['name']})")
	print(f"Lowest average:  {lowest['average']:.2f} ({lowest['name']})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_students(students):
	"""Find and display students whose names contain the search text."""
	search_text = get_text("Enter a student name to search: ")
	if search_text is None:
		print("Search cancelled.")
		return
	matches = [student for student in students
			   if search_text.casefold() in student["name"].casefold()]
	if matches:
		display_students(matches)
	else:
		print(f"No students found matching '{search_text}'.")


def load_students(filename=FILE_NAME):
	"""Load student records from a pipe-delimited file."""
	students = []
	try:
		with open(filename, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					test1, test2, test3, average = map(float, fields[2:6])
				except ValueError:
					print(f"Skipped invalid scores on line {line_number}.")
					continue
				students.append({
					"name": fields[0],
					"id": fields[1],
					"test1": test1,
					"test2": test2,
					"test3": test3,
					"average": average,
					"grade": fields[6],
				})
	except FileNotFoundError:
		print(f"No existing {filename} file found. Starting with no records.")
	except OSError as error:
		print(f"Could not load {filename}: {error}")
	return students


def save_students(students, filename=FILE_NAME):
	"""Save student records in the required pipe-delimited format."""
	try:
		with open(filename, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student['name']}|{student['id']}|"
					f"{student['test1']:.2f}|{student['test2']:.2f}|"
					f"{student['test3']:.2f}|{student['average']:.2f}|"
					f"{student['grade']}\n"
				)
		print(f"Saved {len(students)} student record(s) to {filename}.")
		return True
	except OSError as error:
		print(f"Could not save {filename}: {error}")
		return False


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by student name")
	print("5. Save records")
	print("Press ESC to save and exit")


def main():
	"""Run the interactive student grade calculator."""
	students = load_students()
	while True:
		display_menu()
		try:
			choice = input("Choose an option: ")
		except (EOFError, KeyboardInterrupt):
			print("\nExiting program.")
			save_students(students)
			break

		if is_exit_command(choice):
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_students(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Please choose an option from 1 through 5, or press ESC to exit.")


if __name__ == "__main__":
	main()