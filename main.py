
"""
Application entry point
"""


def main():
    # delegates to main_debug during construction
    import main_debug
    main_debug.main()

if __name__ == "__main__":
    main()
