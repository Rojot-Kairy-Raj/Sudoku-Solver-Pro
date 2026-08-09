// ========================================
// ELEMENTS
// ========================================

const startScreen = document.getElementById("start-screen");
const aboutScreen = document.getElementById("about-screen");
const gameScreen = document.getElementById("game-screen");
const gameBackBtn =
    document.getElementById("game-back-btn");
const startGameBtn = document.getElementById("start-game-btn");
const aboutBtn = document.getElementById("about-btn");
const exitBtn = document.getElementById("exit-btn");

const aboutBackTop = document.getElementById("about-back-top");
const aboutBackBtn = document.getElementById("about-back-btn");
const githubBtn = document.getElementById("github-btn");

const grid = document.getElementById("sudoku-grid");


// ========================================
// START SCREEN
// ========================================

function showStartScreen() {

    startScreen.classList.remove("hidden");
    aboutScreen.classList.add("hidden");
    gameScreen.classList.add("hidden");
}


// ========================================
// ABOUT SCREEN
// ========================================

function showAboutScreen() {

    startScreen.classList.add("hidden");
    aboutScreen.classList.remove("hidden");
    gameScreen.classList.add("hidden");
}


// ========================================
// GAME SCREEN
// ========================================

function showGameScreen() {

    startScreen.classList.add("hidden");
    aboutScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");
}


// ========================================
// BUTTON EVENTS
// ========================================

startGameBtn.addEventListener("click", () => {

    showGameScreen();

    initializeGame();
});
document
    .getElementById("difficulty")
    .addEventListener(
        "change",
        changeDifficulty
    );


aboutBtn.addEventListener("click", () => {

    showAboutScreen();
});


aboutBackTop.addEventListener("click", () => {

    showStartScreen();
});
gameBackBtn.addEventListener(
    "click",
    () => {

        stopTimer();

        gameFinished = true;

        showStartScreen();
    }
);





githubBtn.addEventListener("click", () => {

    window.open(
        "https://github.com/Rojot-Kairy-Raj",
        "_blank"
    );
});


exitBtn.addEventListener("click", () => {

    window.close();

    // Browsers normally block window.close()
    // for tabs that were not opened by JavaScript.
    // Therefore this is only a fallback message.

    setTimeout(() => {

        alert(
            "You can close this browser tab to exit the game."
        );

    }, 100);
});


// ========================================
// SUDOKU VARIABLES
// ========================================

let board = [];
let solution = [];

let lives = 3;

let seconds = 0;
let timerInterval = null;

let gameFinished = false;

let hintsUsed = 0;

let maxHints = 3;


// ========================================
// SOUND
// ========================================

function playSound(file) {

    const sound = new Audio(file);

    sound.volume = 0.8;

    sound.play().catch(error => {

        console.log(
            "Sound could not be played:",
            error
        );

    });
}


// ========================================
// CREATE GRID
// ========================================

function createGrid() {

    grid.innerHTML = "";

    for (let row = 0; row < 9; row++) {

        for (let col = 0; col < 9; col++) {

            const cell =
                document.createElement("input");

            cell.type = "text";

            cell.classList.add(
                "sudoku-cell"
            );

            cell.maxLength = 1;

            cell.inputMode = "numeric";

            cell.dataset.row = row;
            cell.dataset.col = col;

            grid.appendChild(cell);
        }
    }
}


// ========================================
// EMPTY BOARD
// ========================================

function createEmptyBoard() {

    return Array.from(
        { length: 9 },
        () => Array(9).fill(0)
    );
}


// ========================================
// VALIDATE NUMBER
// ========================================

function isValid(board, row, col, num) {

    for (let c = 0; c < 9; c++) {

        if (board[row][c] === num) {
            return false;
        }
    }


    for (let r = 0; r < 9; r++) {

        if (board[r][col] === num) {
            return false;
        }
    }


    const startRow =
        Math.floor(row / 3) * 3;

    const startCol =
        Math.floor(col / 3) * 3;


    for (
        let r = startRow;
        r < startRow + 3;
        r++
    ) {

        for (
            let c = startCol;
            c < startCol + 3;
            c++
        ) {

            if (
                board[r][c] === num
            ) {

                return false;
            }
        }
    }

    return true;
}


// ========================================
// SOLVE SUDOKU
// ========================================

function solveSudoku(board) {

    for (let row = 0; row < 9; row++) {

        for (let col = 0; col < 9; col++) {

            if (board[row][col] === 0) {

                const numbers = [
                    1, 2, 3, 4, 5,
                    6, 7, 8, 9
                ];

                numbers.sort(
                    () => Math.random() - 0.5
                );


                for (const num of numbers) {

                    if (
                        isValid(
                            board,
                            row,
                            col,
                            num
                        )
                    ) {

                        board[row][col] = num;


                        if (
                            solveSudoku(board)
                        ) {

                            return true;
                        }


                        board[row][col] = 0;
                    }
                }


                return false;
            }
        }
    }

    return true;
}


// ========================================
// GENERATE PUZZLE
// ========================================

function countSolutions(board, limit = 2) {

    let count = 0;

    function solve() {

        if (count >= limit) {
            return;
        }

        let bestRow = -1;
        let bestCol = -1;
        let bestCandidates = null;

        for (let row = 0; row < 9; row++) {

            for (let col = 0; col < 9; col++) {

                if (board[row][col] === 0) {

                    const candidates = [];

                    for (let num = 1; num <= 9; num++) {

                        if (
                            isValid(
                                board,
                                row,
                                col,
                                num
                            )
                        ) {
                            candidates.push(num);
                        }
                    }

                    if (candidates.length === 0) {
                        return;
                    }

                    if (
                        bestCandidates === null ||
                        candidates.length <
                        bestCandidates.length
                    ) {
                        bestCandidates = candidates;
                        bestRow = row;
                        bestCol = col;
                    }
                }
            }
        }

        if (bestCandidates === null) {
            count++;
            return;
        }

        for (const num of bestCandidates) {

            board[bestRow][bestCol] = num;

            solve();

            board[bestRow][bestCol] = 0;

            if (count >= limit) {
                return;
            }
        }
    }

    solve();

    return count;
}


function generatePuzzle(difficulty) {

    let removeCount;

    if (difficulty === "Easy") {

        removeCount = 35;

    } else if (difficulty === "Hard") {

        removeCount = 52;

    } else {

        removeCount = 45;
    }

    while (true) {

        solution = createEmptyBoard();

        solveSudoku(solution);

        board = solution.map(
            row => [...row]
        );

        const positions = [];

        for (let row = 0; row < 9; row++) {

            for (let col = 0; col < 9; col++) {

                positions.push([row, col]);
            }
        }

        positions.sort(
            () => Math.random() - 0.5
        );

        let removed = 0;

        for (const [row, col] of positions) {

            if (removed >= removeCount) {
                break;
            }

            const backup =
                board[row][col];

            board[row][col] = 0;

            const testBoard =
                board.map(
                    row => [...row]
                );

            const solutions =
                countSolutions(
                    testBoard,
                    2
                );

            if (solutions === 1) {

                removed++;

            } else {

                board[row][col] = backup;
            }
        }

        if (removed === removeCount) {
            return board;
        }
    }
}


// ========================================
// DISPLAY PUZZLE
// ========================================

function displayPuzzle(puzzle) {

    const cells =
        document.querySelectorAll(
            ".sudoku-cell"
        );


    cells.forEach(cell => {

        const row =
            Number(cell.dataset.row);

        const col =
            Number(cell.dataset.col);


        cell.value = "";

        cell.readOnly = false;


        cell.classList.remove(
            "given",
            "correct",
            "wrong"
        );


        if (
            puzzle[row][col] !== 0
        ) {

            cell.value =
                puzzle[row][col];

            cell.readOnly = true;

            cell.classList.add(
                "given"
            );
        }
    });
}


// ========================================
// LIVES
// ========================================

function updateLives() {

    const livesElement =
        document.getElementById("lives");


    let display = "";


    for (let i = 0; i < 3; i++) {

        if (i < lives) {

            display += "♥";

        } else {

            display += "♡";
        }
    }


    livesElement.textContent =
        display;
}


// ========================================
// TIMER
// ========================================

function formatTime(totalSeconds) {

    const minutes =
        Math.floor(totalSeconds / 60);

    const remainingSeconds =
        totalSeconds % 60;


    return (
        String(minutes).padStart(2, "0") +
        ":" +
        String(remainingSeconds).padStart(2, "0")
    );
}


function updateTimer() {

    document.getElementById(
        "timer"
    ).textContent =
        "⏱ " + formatTime(seconds);
}


function startTimer() {

    stopTimer();

    timerInterval =
        setInterval(() => {

            if (!gameFinished) {

                seconds++;

                updateTimer();
            }

        }, 1000);
}


function stopTimer() {

    if (timerInterval !== null) {

        clearInterval(timerInterval);

        timerInterval = null;
    }
}


// ========================================
// INPUT VALIDATION
// ========================================
// ========================================
// HIGHLIGHT SAME NUMBERS
// ========================================

function highlightSameNumbers(selectedCell) {

    document
        .querySelectorAll(".sudoku-cell")
        .forEach(cell => {
            cell.classList.remove(
                "same-number-highlight"
            );
        });

    const selectedValue =
        selectedCell.value;

    if (!selectedValue) {
        return;
    }

    document
        .querySelectorAll(".sudoku-cell")
        .forEach(cell => {

            if (cell.value === selectedValue) {

                cell.classList.add(
                    "same-number-highlight"
                );
            }
        });
}
function attachInputEvents() {

    const cells =
        document.querySelectorAll(
            ".sudoku-cell"
        );


    cells.forEach(cell => {

    cell.onclick = function () {

        highlightSameNumbers(this);

    };


    cell.oninput = function () {

            if (gameFinished) {

                this.value = "";

                return;
            }


            this.value =
                this.value.replace(
                    /[^1-9]/g,
                    ""
                );


            if (this.value !== "") {

                checkInput(this);
                if (
    this.classList.contains("correct")
) {

    highlightSameNumbers(this);

}
            }
        };
    });
}


// ========================================
// CHECK INPUT
// ========================================

function checkInput(cell) {

    const row =
        Number(cell.dataset.row);

    const col =
        Number(cell.dataset.col);

    const value =
        Number(cell.value);


    if (!value) {
        return;
    }


    // CORRECT
    if (
        value === solution[row][col]
    ) {

       cell.classList.remove(
    "given",
    "correct",
    "wrong"
);

        cell.classList.add(
            "correct"
        );

        cell.readOnly = true;


        document.getElementById(
            "status-text"
        ).textContent =
            "Status : Correct";


        updateRemainingNumbers();


        if (checkWin()) {

            showWinPopup();
        }

    }

    // WRONG
    else {

        cell.classList.add(
            "wrong"
        );

        lives--;

        updateLives();

        playSound(
            "../assets/sounds/wrong.wav"
        );


        document.getElementById(
            "status-text"
        ).textContent =
            "Status : Wrong number";


        setTimeout(() => {

            cell.value = "";

            cell.classList.remove(
                "wrong"
            );

        }, 500);


        if (lives <= 0) {

            showGameOverPopup();
        }
    }
}


// ========================================
// CHECK WIN
// ========================================

function checkWin() {

    const cells =
        document.querySelectorAll(
            ".sudoku-cell"
        );


    for (const cell of cells) {

        const row =
            Number(cell.dataset.row);

        const col =
            Number(cell.dataset.col);


        if (
            Number(cell.value) !==
            solution[row][col]
        ) {

            return false;
        }
    }


    return true;
}


// ========================================
// REMAINING NUMBERS
// ========================================

function updateRemainingNumbers() {

    const cells =
        document.querySelectorAll(
            ".sudoku-cell"
        );


    const counts = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0
    };


    cells.forEach(cell => {

        const value =
            Number(cell.value);


        if (
            value >= 1 &&
            value <= 9
        ) {

            counts[value]++;
        }
    });


    for (let number = 1; number <= 9; number++) {

        const item =
            document.querySelector(
                `.remaining-item[data-number="${number}"]`
            );


        if (!item) {
            continue;
        }


        const remaining =
            9 - counts[number];


        item.textContent =
            `${number} : ${remaining}`;


        item.classList.remove(
            "zero",
            "low",
            "medium",
            "high",
            "very-high"
        );


        if (remaining === 0) {

            item.classList.add("zero");

        } else if (remaining <= 2) {

            item.classList.add("low");

        } else if (remaining <= 4) {

            item.classList.add("medium");

        } else if (remaining <= 6) {

            item.classList.add("high");

        } else {

            item.classList.add(
                "very-high"
            );
        }
    }
}


// ========================================
// HINT LIMIT
// ========================================

function updateHintButton() {

    const button =
        document.getElementById(
            "hint-btn"
        );


    button.textContent =
        `Hint (${maxHints - hintsUsed})`;
}


// ========================================
// NEW GAME
// ========================================

function startNewGame() {

    stopTimer();

    lives = 3;
    seconds = 0;
    hintsUsed = 0;
    gameFinished = false;

    const difficulty =
        document.getElementById("difficulty").value;

    const puzzle =
        generatePuzzle(difficulty);

    displayPuzzle(puzzle);

    attachInputEvents();

    updateLives();
    updateTimer();
    updateHintButton();
    updateRemainingNumbers();

    document.getElementById(
        "status-text"
    ).textContent =
        "Status : New Puzzle Generated";

    startTimer();
}
// ========================================
// RESTART CURRENT GAME
// ========================================

function restartGame() {

    stopTimer();

    lives = 3;
    seconds = 0;
    hintsUsed = 0;
    gameFinished = false;


    // Keep the SAME puzzle.
    // Only clear the player's answers.

    const cells =
        document.querySelectorAll(
            ".sudoku-cell"
        );


    cells.forEach(cell => {

        const row =
            Number(cell.dataset.row);

        const col =
            Number(cell.dataset.col);


        // Original given number
        // stays unchanged

        if (board[row][col] !== 0) {

            cell.value =
                board[row][col];

            cell.readOnly = true;

            cell.classList.remove(
                "wrong",
                "correct"
            );

            cell.classList.add(
                "given"
            );

        } else {

            // Player-entered number
            // gets cleared

            cell.value = "";

            cell.readOnly = false;

            cell.classList.remove(
                "wrong",
                "correct",
                "given"
            );
        }
    });


    updateLives();
    updateTimer();
    updateHintButton();
    updateRemainingNumbers();


    document.getElementById(
        "status-text"
    ).textContent =
        "Status : Game Restarted";


    startTimer();
}
// ========================================
// DIFFICULTY CHANGE
// ========================================

let currentDifficulty = "Medium";

function changeDifficulty() {

    const select =
        document.getElementById("difficulty");

    const newDifficulty = select.value;

    if (newDifficulty === currentDifficulty) {
        return;
    }

    // If no game has started yet
    if (!board.length) {

        currentDifficulty = newDifficulty;

        updateHintLimit();

        startNewGame();

        return;
    }

    const oldDifficulty = currentDifficulty;

    const popup =
        document.getElementById("popup-container");

    popup.innerHTML = `
        <div class="popup-box">

            <div class="popup-title">
                Change Difficulty?
            </div>

            <div class="popup-message">
                Your current game progress<br>
                will be lost.
            </div>

            <div class="popup-buttons">

                <button
                    id="difficulty-continue"
                    class="popup-button"
                >
                    Continue
                </button>

                <button
                    id="difficulty-cancel"
                    class="popup-button cancel"
                >
                    Cancel
                </button>

            </div>

        </div>
    `;

    popup.classList.remove("hidden");


    document
        .getElementById("difficulty-continue")
        .onclick = () => {

            popup.classList.add("hidden");

            currentDifficulty =
                newDifficulty;

            updateHintLimit();

            startNewGame();
        };


    document
        .getElementById("difficulty-cancel")
        .onclick = () => {

            popup.classList.add("hidden");

            select.value =
                oldDifficulty;
        };
}
function updateHintLimit() {

    if (currentDifficulty === "Easy") {

        maxHints = 5;

    } else if (currentDifficulty === "Medium") {

        maxHints = 3;

    } else {

        maxHints = 2;
    }

    hintsUsed = 0;

    updateHintButton();
}


// ========================================
// GENERATE BUTTON
// ========================================

document
    .getElementById("generate-btn")
    .addEventListener(
        "click",
        startNewGame
    );


// ========================================
// RESTART BUTTON
// ========================================

document
    .getElementById("restart-btn")
    .addEventListener(
        "click",
        restartGame
    );


// ========================================
// SOLVE BUTTON
// ========================================

document
    .getElementById("solve-btn")
    .addEventListener(
        "click",
        () => {

            if (gameFinished) {
                return;
            }

            const cells =
                document.querySelectorAll(
                    ".sudoku-cell"
                );


            // Show complete solution
            cells.forEach(cell => {

                const row =
                    Number(cell.dataset.row);

                const col =
                    Number(cell.dataset.col);


                cell.value =
                    solution[row][col];

                cell.readOnly = true;

                cell.classList.remove(
                    "wrong"
                );

                cell.classList.add(
                    "correct"
                );
            });


            updateRemainingNumbers();


            document.getElementById(
                "status-text"
            ).textContent =
                "Status : Solution shown";


            // Stop current game temporarily
            gameFinished = true;

            stopTimer();


            // Wait 3 seconds, then start
            // a completely new puzzle

            setTimeout(() => {

                gameFinished = false;

                startNewGame();

            }, 3000);
        }
    );


// ========================================
// HINT BUTTON
// ========================================

document
    .getElementById("hint-btn")
    .addEventListener(
        "click",
        useHint
    );


function useHint() {

    if (gameFinished) {
        return;
    }


    if (hintsUsed >= maxHints) {

        document.getElementById(
            "status-text"
        ).textContent =
            "Status : No hints remaining";

        return;
    }


    const emptyCells = [];


    document
        .querySelectorAll(
            ".sudoku-cell"
        )
        .forEach(cell => {

            if (
                !cell.value &&
                !cell.readOnly
            ) {

                emptyCells.push(cell);
            }
        });


    if (emptyCells.length === 0) {
        return;
    }


    const cell =
        emptyCells[
            Math.floor(
                Math.random() *
                emptyCells.length
            )
        ];


    const row =
        Number(cell.dataset.row);

    const col =
        Number(cell.dataset.col);


    cell.value =
        solution[row][col];

    cell.readOnly = true;

    cell.classList.add(
        "correct"
    );


    hintsUsed++;

    updateHintButton();

    updateRemainingNumbers();


    document.getElementById(
        "status-text"
    ).textContent =
        "Status : Hint used";


    if (checkWin()) {

        showWinPopup();
    }
}


// ========================================
// WIN POPUP
// ========================================

function showWinPopup() {

    gameFinished = true;

    stopTimer();

    playSound(
        "../assets/sounds/win.wav"
    );


    const popup =
        document.getElementById(
            "popup-container"
        );


    popup.innerHTML = `
        <div class="popup-box">

            <div class="popup-title">
                Congratulations!
            </div>

            <div class="popup-message">
                You solved the Sudoku puzzle!
            </div>

            <div class="popup-info">
                Time : ${formatTime(seconds)}
            </div>

            <div class="popup-info">
                Lives Left : ${lives}
            </div>

            <div class="popup-info">
                Hints Used : ${hintsUsed}
            </div>

            <div class="popup-rating">
                ★★★★★
            </div>

            <div class="popup-buttons">

                <button
                    id="popup-new-game"
                    class="popup-button"
                >
                    New Game
                </button>

                <button
                    id="popup-close"
                    class="popup-button cancel"
                >
                    Close
                </button>

            </div>

        </div>
    `;


    popup.classList.remove(
        "hidden"
    );


    document
        .getElementById(
            "popup-new-game"
        )
        .onclick = () => {

            popup.classList.add(
                "hidden"
            );

            startNewGame();
        };


    document
        .getElementById(
            "popup-close"
        )
        .onclick = () => {

            popup.classList.add(
                "hidden"
            );
        };
}


// ========================================
// GAME OVER POPUP
// ========================================

function showGameOverPopup() {

    gameFinished = true;

    stopTimer();


    playSound(
        "../assets/sounds/game_over.wav"
    );


    const popup =
        document.getElementById(
            "popup-container"
        );


    const difficulty =
        document.getElementById(
            "difficulty"
        ).value;


    popup.innerHTML = `
        <div class="popup-box">

            <div class="popup-title">
                Game Over
            </div>

            <div class="popup-message">
                You ran out of lives!
            </div>

            <div class="popup-info">
                Difficulty : ${difficulty}
            </div>

            <div class="popup-info">
                Time : ${formatTime(seconds)}
            </div>

            <div class="popup-info">
                Hints Used : ${hintsUsed}
            </div>

            <div class="popup-buttons">

                <button
                    id="popup-restart"
                    class="popup-button"
                >
                    Restart
                </button>

                <button
                    id="popup-close"
                    class="popup-button cancel"
                >
                    Close
                </button>

            </div>

        </div>
    `;


    popup.classList.remove(
        "hidden"
    );


    document
        .getElementById(
            "popup-restart"
        )
        .onclick = () => {

            popup.classList.add(
                "hidden"
            );

            startNewGame();
        };


    document
        .getElementById(
            "popup-close"
        )
        .onclick = () => {

            popup.classList.add(
                "hidden"
            );
        };
}


// ========================================
// INITIALIZE
// ========================================

createGrid();

updateLives();

showStartScreen();

