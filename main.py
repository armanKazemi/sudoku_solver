from ai import AI

if __name__ == '__main__':
    model = AI()
    data = '{"sudoku": [[1,0,4,8,6,5,2,3,7],[7,0,5,4,1,2,9,6,8],[8,0,2,3,9,7,1,4,5],[9,0,1,7,4,8,3,5,6],[6,0,8,5,3,1,4,2,9],[4,0,3,9,2,6,8,7,1],[3,0,9,6,5,4,7,1,2],[2,0,6,1,7,9,5,8,3],[5,0,7,2,8,3,6,9,4]]}'
    result = model.solve(data)
    for row in result:
        print(row)
