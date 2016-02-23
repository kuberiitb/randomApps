## Objective: Solve a sudoku Puzzle in R(beta)

Puzzle in text form has been obtained from [projecteuler](https://projecteuler.net/project/resources/p096_sudoku.txt)

* Read puzzle
```{R}
# given puzzleid, read puzzle from file downloaded from projecteuler file
readPuzzle<-function(puzzleid='01'){
  #read a puzzle
  pfile = readLines('C:\\Users\\Kuber Churasiya\\Downloads\\temp\\sudoku\\p096_sudoku.txt')
  copy = 0
  puzzletext = character()
  for(line in pfile){
    if(grepl("Grid", line)){
      if( line == paste("Grid", puzzleid ) ){
        print(line)
        copy=1
      }
      else{copy=0}
    }
    if(copy>0){
      puzzletext<-c(puzzletext,line)}
      #print(puzzletext)
  }
  
  print(puzzletext)
  puzzlemat = matrix(0,9,9)
  print(puzzlemat)
  for(i in 1:9){
    for(j in 1:9){
      puzzlemat[i,j] = as.integer(substr(puzzletext[i+1],j,j))
    }
  }
  print(puzzlemat)
  return(puzzlemat)
}
#test it
pm = readPuzzle('02')
print(pm)
```

* Define some functions to be used later
```{R}
# return the 3x3 sub-block for given sudoku and index
getBlock<-function(mat, i,j){
  istart = ((i-1)%/%3)*3+1
  iend   = ((i-1)%/%3)*3+3
  jstart = ((j-1)%/%3)*3+1
  jend   = ((j-1)%/%3)*3+3
  return(mat[istart:iend, jstart:jend])
}
#test it
getBlock(pm, i,j)
```

```{R}
# return possible options left for the given sudoku at given index
checkOptions <- function(mat, row, col){
  done = unique(c(mat[row,][mat[row,]>0], mat[,col][mat[,col]>0], array(getBlock(mat, row, col)) ) )
  #print(done)
  left = setdiff(1:9, done)
  return(left)
}
#test it
checkOptions(pm,1,2)
```

```{R}
# checks if the given sudoku is complete and correct
checkSudoku<-function(mat){
  dimCheck = all(dim(mat) == c(9,9))
  rowCheck = 0
  for(row in 1:9){
    if( all(sort(mat[row,]) == 1:9) )
      rowCheck = rowCheck + 1
  }
  colCheck = 0
  for(col in 1:9){
    if( sum(sort(mat[,col]) == 1:9) )
      colCheck = colCheck + 1
  }
  blockCheck = 0
  for(i in seq(1,9,3)){
    for(j in seq(1,9,3) ){
      if( all(sort(array(getBlock(pm, i, j )))==1:9) )
        blockCheck = blockCheck + 1
    }
  }  
  
  print(c(dimCheck, rowCheck==9, colCheck==9, blockCheck==9))
  return(all(dimCheck, rowCheck==9, colCheck==9, blockCheck==9))
}
checkSudoku(pm)
```

##Finally, Main function

```{R}

solveSudoku<-function(mat){
  iteratins = 0
  solvable = 1
  while(solvable>0){
    iteratins = iteratins + 1
    cat(paste("Iteratin:", iteratins, "\n"))
    solvable=0
    Sys.sleep(1)
    
    for(i in 1:9){
      for(j in 1:9){
        if(mat[i,j]==0){
          solution = checkOptions(mat, i, j)
          cat(paste("Fill (", i, j, ") "))
          cat(solution, '\n')
          if(length(solution)==1){
            mat[i,j] <- solution
            solvable=1
            #print(mat[i,j])
          }
          else{
            #cat(paste("Fill Multiple (", i, j, ") "))
            #cat(solution, '\n')
          }
        }
      }
    }
  }
  if(solvable==0){
    if(min(mat)){
      cat(paste("Solved in ", iteratins, "iteratins.", "\n"))
      }
    else{
      cat(paste("Could Not Solve in",iteratins, "iteratins", "\n"))
      }
}
return(mat)
}
```

*Test it on any puzzle
```{R}
solveSudoku(pm)
>>Solved in  8 iteratins.
```
*Or any other puzzle with given id (01 - 50)
```{R}
solveSudoku(readPuzzle('01'))
>>Solved in  8 iteratins.
```
## Improvements to be made
This code solves some of the problems(eg 01, 05..) but not all. 

It stucks at point when no cell is left with unique option and one need to try one of the options to proceed further.

I will fix the bug and update the code soon.

Till then, Tell me how may, of the 50 puzzles, this code could solve(Don't run a loop, OK?)
