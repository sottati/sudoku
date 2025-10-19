from utils import print_matrix, initialize_matrix, populate_matrix

def main():
    matrix = initialize_matrix()
    populate_matrix(matrix)
    print_matrix(matrix)

if __name__ == "__main__":
    main()