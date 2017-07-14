
"""
Application entry point
"""


def main():
    pass

if __name__ == "__main__":
    # delegates to main_debug during construction
    try:
        import main_debug
        main_debug.main()
    except ImportError:
        main()
