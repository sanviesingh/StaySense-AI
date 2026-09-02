"""Calculate the average laboratory exam score per session."""

import math


def calculate_lab_metrics() -> None:
    print("==================================================")
    print("   B.TECH LABORATORY EXAM ASSESSMENT MODULE")
    print("==================================================")
    
    try:
        # Prompting user input for raw numerical performance values
        raw_score_input = input("Enter total marks secured in laboratory exams: ")
        total_score = float(raw_score_input)
        if not math.isfinite(total_score) or total_score < 0:
            raise ValueError("Total marks must be a finite, non-negative number.")
        
        raw_count_input = input("Enter total number of lab sessions conducted: ")
        session_count = int(raw_count_input)
        
        # Validating potential division by zero condition logically
        if session_count <= 0:
            raise ValueError("Session count must be greater than zero.")
            
        # Mathematical derivation of final performance averages
        average_score = total_score / session_count
        
        print("\n--------------------------------------------------")
        print("EXECUTION SUCCESS: Laboratory evaluation processed.")
        print(f"Computed Performance Average: {average_score:.2f} marks per session.")
        print("--------------------------------------------------")
        
    except ValueError as val_error:
        print("\n--------------------------------------------------")
        print(f"INPUT ERROR: Invalid numerical format detected.")
        print(f"Details: {val_error}")
        print("--------------------------------------------------")
        
    except Exception as general_error:
        print("\n--------------------------------------------------")
        print("UNEXPECTED RUNTIME FAULT OCCURRED.")
        print(f"System Log: {general_error}")
        print("--------------------------------------------------")
        
    finally:
        print("Assessing routine terminated. Returning back to core system execution stack.")


def main() -> None:
    calculate_lab_metrics()


if __name__ == "__main__":
    main()
