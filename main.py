import services
import exceptions


# Обработчик проверки типа введенных данных
def action_check_input_type() -> None:
    raw_input = input("Enter data (URL, file path, or string): ").strip()
    if not raw_input:
        print("Input cannot be empty")
        return

    input_type = services.parsing_input(raw_input)
    print(f"Detected input type: {input_type}")


# Обработчик извлечения и вывода комментариев из выбранного источника
def action_extract_comments() -> None:
    raw_input = input("Enter source (URL, file path, or code string): ").strip()
    if not raw_input:
        print("Input cannot be empty")
        return

    try:
        comments = services.get_comments(raw_input)
        if not comments:
            print("No comments found")
            return

        print(f"\nFound comments ({len(comments)}):")
        for idx, comment in enumerate(comments, start=1):
            print(f"[{idx}] {comment}")
    except exceptions.NetworkAccessError as e:
        print(f"Network error: {e}")
    except exceptions.FileReadError as e:
        print(f"File access error: {e}")
    except exceptions.BusinessLogicError as e:
        print(f"Business logic error: {e}")


# Главное консольное меню и точка входа в программу
def main() -> None:
    while True:
        print("\n=== COMMENT EXTRACTOR SYSTEM ===")
        print("[1] Check input type")
        print("[2] Extract comments (URL, file, or string)")
        print("[0] Exit")

        choice = input("Select an action: ").strip()
        if choice == "1":
            action_check_input_type()
        elif choice == "2":
            action_extract_comments()
        elif choice == "0":
            break
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()