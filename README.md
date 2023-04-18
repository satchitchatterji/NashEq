# Nash Equilibrium Finder (Limited)

*This code was originally a solution to an exercise for [ILLC's Game Theory Course 2023](https://staff.science.uva.nl/u.endriss/teaching/game-theory/) at the University of Amsterdam. Thus, this readme is a bit extensive and is public for the sake of instruction*.

The goal of the program is to compute the pure and mixed Nash equilibria in two-player two-action games with at least finitely many mixed strategies. An explaination of possible extentions to infinite mixed Nash equilibria is discussed briefly at the end of this readme. The solution of how the code is implemented is discussed here in full.

---

The code for this exercise was written in Python 3.10.7 and only requires NumPy as a dependency.

## Representation
The utility matrix is represented as a single string, with integer payoff values delimited by commas: `a,b,c,d,e,f,g,h` . The first four values are the payoffs for row player, and the next four are the payoffs for the column player. The values in this string should correspond to the following payoff matrix:
\begin{center}
\nfgame{T B L R $a$ $b$ $c$  $d$
                $e$ $f$ $g$ $h$}
\end{center}

**Usage:** Thus, the code should be run by calling in the terminal:

    python solve_nash.py a,b,c,d,e,f,g,h

For example, running the code on a known example gives us the following output:

    $ python solve_nash.py 5,6,2,9,9,3,2,5
    Payoffs: 5,6,2,9,9,3,2,5
     Table form:
                    | 5\9 | 6\3 |
                    |-----|-----|
                    | 2\2 | 9\5 |

    Pure Nash equilibium : [(0, 0), (1, 1)]
    Mixed Nash equilibium: (0.3333333333333333, 0.5)

The pure Nash equilibrium are coordinates for the matrix (in this case the cells at the top left and the bottom right) and the mixed NE are the probability values of the players for respectively playing their first action (i.e. top and left respectively for the row and column player). For this game, the output matches the expected result when computing NE by hand. The program was verified in this way for several known games successfully.

## Finding Pure Nash Equilibria

The function `find_pure_ne` computes all the pure Nash equilibria in the input 2x2 game. It does this by following the definition of a pure NE. It finds these by iterating through each cell in the matrix and verifying whether the payoff for the row player in that cell is *at least* as high as the payoff in the cells above or below it. This is equivalent to checking whether the row player has an incentive to change their play, given the column player has played their action. Similarly, the column player's payoff is compared to the payoffs to the right or left of it for the same reason. If this cell's payoff provides a utility that is at least as high as it's respective neighbouring cells' utilities for each player, then it is considered a Nash equilibrium. Since this is a small game (2x2) iterating through all possibilities is trivial -- however, for a larger game (more players or actions), the space of possibilities grows exponentially. Thus, in this case, better heuristics or strategies such as IESDS may be implemented to assist in reducing computation time.

## Finding Mixed Nash Equilibria
The function `find_mixed_ne` computes the finite mixed Nash equilibria in the input 2x2 game if it exists. Since we are looking for a Nash equilibrium, the column player must be indifferent to the action he takes: i.e. his utilities for choosing L and R should be the same, regardless of what the row player plays. If the probability of choosing L is $p$, this can be computed directly as:

$$ e\cdot p + g\cdot(1-p) = f\cdot p + h\cdot(1-p)$$

$$ p =\frac{h-g}{e-f-g+h}$$

Similar reasoning may be conducted for the row player. If the probability of them choosing T if $q$, it may be computed as:

$$ a \cdot q + b\cdot(1-q) = c\cdot q + d\cdot(1-q)$$

$$ q =\frac{d-b}{a-c-b+d}$$

However, this direct computation has a few caveats, since there is no restriction on the payoffs in the 2x2 matrix. Firstly, the denominators in both of these fractions should not be zero. In this case, no mixed NE exist. Secondly, if the resulting values of $p$ or $q$ are greater than 1 or less than 0, this cannot be a probability, and thus no mixed NE exist. Finally, if $p\in[0,1]$ and $q\in[0,1]$, and we compute and output it as such. 

In this final case, it may not be the case that there only exists one Nash equilibria, but infinitely many, e.g. due to the fact that one player may extract the same utility by playing their actions within a continuous range of probabilities (e.g. in the case of equal strictly dominating strategies). This is not taken into account in this script. However, it may be generalised in a number of ways. One way is to compute the mixed NE, and then simulate playing for values $p\pm \epsilon$ and $q\pm \epsilon$ for some small value(s) $\epsilon$. This simulates human reasoning (*"What if Colin plays L more often than the critical value. Does Rowina's strategy change?"*). However, depending on the choice of $\epsilon$, there may be a tradeoff between not finding the bounds of the infinite mixed strategies (since $\epsilon$ is necessarily rational in the case of computers), and computation time.

Other ways that may be possible to implement were found in papers such as Avis *et al.* (2010) (polyhedral vertex enumeration), Widger & Grosu (2008) (parallel support enumeration) or Lemke & Howson, (1964) (the Lemke-Howson algorithm). However, these were not explored further in this repository.

---
## Additional References
Avis, D., Rosenberg, G. D., Savani, R., \& Von Stengel, B. (2010). \textit{Enumeration of Nash Equilibria for Two-player Games}. Economic Theory, 42, 9-37.

Widger, J., \& Grosu, D. (2008, July). \textit{Computing Equilibria in Bimatrix Games by Parallel Support Enumeration}. In 2008 International Symposium on Parallel and Distributed Computing (pp. 250-256). IEEE.

Lemke, C. E., \& Howson, Jr, J. T. (1964). \textit{Equilibrium Points of Bimatrix Games}. Journal of the Society for Industrial and Applied Mathematics, 12(2), 413-423.
