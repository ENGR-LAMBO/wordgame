// index.js
document.addEventListener('DOMContentLoaded', () => {
    const letterGrid = document.querySelector('.letter-grid');
    const scoreSpan = document.querySelector('.score');
    const timerElement = document.getElementById('time');
    const timeupPopup = document.getElementById('timeup-popup');
    const winPopup = document.getElementById('win-popup');
    const reloadTimeupButton = document.getElementById('reload-timeup');
    const nextLevelTimeupButton = document.getElementById('next-level-timeup');
    const reloadWinButton = document.getElementById('reload-win');
    const nextLevelWinButton = document.getElementById('next-level-win');
    const words = ["CAT", "DOG", "MOUSE", "BIRD", "FISH", "HOUSE", "TREE", "CAR", "BIKE", "LAMP", "AARDVARK", "APPLE", "BANANA", "BASKET", "CAT", "CANDLE", "DOG", "DOLPHIN", "ELEPHANT", "EGG",
    "FOX", "FROG", "GIRAFFE", "GUITAR", "HOUSE", "HAT", "CREAM", "ISLAND","JAGUAR", "JACKET",
    "KANGAROO", "KEY", "LION", "LAMP", "MONKEY", "MOON", "NOTEBOOK", "NECKLACE", "OSTRICH", "ORANGE",
    "PARROT", "PIANO", "QUILT", "QUEEN", "RABBIT", "RAINBOW","STAR", "SOFA", "TIGER", "TABLE",
    "UMBRELLA", "UNICORN", "VIOLIN", "VASE", "WHALE", "WATCH", "XYLOPHONE", "YAK", "YACHT",
    "ZEBRA", "ZOO", "LAND", "ALE", "QUEUE", "MAN", "WOMAN", "KID", "CHILD", "YOGURT", "MILK", "WAND", "STOOL", "ROBBER", "GENDER", "FOOTBALL", "ROOKIE", "NOVICE", "BEGINNER", "EXPERT", "ULTIMATE", "LEGEND", "GAME"];
    const gridLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const selectedCells = [];
    let score = 0;
    let timeRemaining = 60; // 1 minute countdown
    const colorClasses = ['light-blue', 'pink', 'light-green', 'light-red'];
    const rows = 7;
    const cols = 7;

    const updateTimer = () => {
        if (timeRemaining <= 0) {
            timeupPopup.classList.add('show');
            return;
        }
        timeRemaining--;
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        timerElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    };

    setInterval(updateTimer, 1000);

    const grid = Array.from({ length: rows }, () => Array(cols).fill(null));

    const placeWordsOnGrid = () => {
        let wordsPlaced = 0;
        while (wordsPlaced < 6) {
            const word = words[Math.floor(Math.random() * words.length)];
            const direction = Math.random() > 0.5 ? 'horizontal' : 'vertical';
            let row, col, fits;

            if (direction === 'horizontal') {
                row = Math.floor(Math.random() * rows);
                col = Math.floor(Math.random() * (cols - word.length));
                fits = true;
                for (let i = 0; i < word.length; i++) {
                    if (grid[row][col + i] !== null) {
                        fits = false;
                        break;
                    }
                }
                if (fits) {
                    for (let i = 0; i < word.length; i++) {
                        grid[row][col + i] = word[i];
                    }
                    wordsPlaced++;
                }
            } else {
                row = Math.floor(Math.random() * (rows - word.length));
                col = Math.floor(Math.random() * cols);
                fits = true;
                for (let i = 0; i < word.length; i++) {
                    if (grid[row + i][col] !== null) {
                        fits = false;
                        break;
                    }
                }
                if (fits) {
                    for (let i = 0; i < word.length; i++) {
                        grid[row + i][col] = word[i];
                    }
                    wordsPlaced++;
                }
            }
        }
    };

    const fillGridWithRandomLetters = () => {
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                if (grid[row][col] === null) {
                    grid[row][col] = gridLetters.charAt(Math.floor(Math.random() * gridLetters.length));
                }
            }
        }
    };

    placeWordsOnGrid();
    fillGridWithRandomLetters();

    const createGridInDOM = () => {
        letterGrid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
        letterGrid.style.gridTemplateRows = `repeat(${rows}, 1fr)`;

        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const letterCell = document.createElement('div');
                letterCell.classList.add('letter-cell');
                letterCell.textContent = grid[row][col];
                letterGrid.appendChild(letterCell);
            }
        }
    };

    createGridInDOM();

    const validateWord = () => {
        const selectedWord = selectedCells.map(cell => cell.textContent).join('');
        if (words.includes(selectedWord)) {
            const colorClass = colorClasses[Math.floor(Math.random() * colorClasses.length)];
            selectedCells.forEach(cell => {
                cell.classList.add('validated', colorClass);
                cell.classList.remove('clicked');
            });
            score += selectedWord.length * 3;
            scoreSpan.textContent = score;
            selectedCells.length = 0;
        }
    };

    letterGrid.addEventListener('click', (event) => {
        const clickedCell = event.target;

        if (clickedCell.classList.contains('letter-cell')) {
            if (clickedCell.classList.contains('validated')) return;

            clickedCell.classList.toggle('clicked');

            if (clickedCell.classList.contains('clicked')) {
                selectedCells.push(clickedCell);
            } else {
                const index = selectedCells.indexOf(clickedCell);
                if (index > -1) selectedCells.splice(index, 1);
            }

            if (selectedCells.length > 1) {
                const lastCell = selectedCells[selectedCells.length - 1];
                const secondLastCell = selectedCells[selectedCells.length - 2];
                const lastCellIndex = Array.from(letterGrid.children).indexOf(lastCell);
                const secondLastCellIndex = Array.from(letterGrid.children).indexOf(secondLastCell);
                if (Math.abs(lastCellIndex - secondLastCellIndex) !== 1 && Math.abs(lastCellIndex - secondLastCellIndex) !== cols) {
                    lastCell.classList.remove('clicked');
                    selectedCells.pop();
                }
            }

            if (selectedCells.length >= 3) {
                validateWord();
            }
        }
    });

    reloadTimeupButton.addEventListener('click', () => location.reload());
    nextLevelTimeupButton.addEventListener('click', () => window.location.href = './level2.html');
    reloadWinButton.addEventListener('click', () => location.reload());
    nextLevelWinButton.addEventListener('click', () => window.location.href = './level2.html');
});
