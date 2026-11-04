import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output

def test_main():
    calculator = Calculator()
    expression = "3 + 5"
    try:
        result = calculator.evaluate(expression)
        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_main()