function executeBacktest() {
    const positionsFile = document.getElementById('positionsFile').files[0];
    const pricesFile = document.getElementById('pricesFile').files[0];
    const takeProfit = document.getElementById('takeProfit').value;
    const stopLoss = document.getElementById('stopLoss').value;
    const outputName = document.getElementById('outputName').value;

    if (!positionsFile || !pricesFile) {
        alert('Proszę wybrać oba pliki.');
        return;
    }

    if (!takeProfit || !stopLoss || !outputName) {
        alert('Proszę wprowadzić wartości Take profit, Stop loss i Output name.');
        return;
    }

    if (!Number.isInteger(Number(takeProfit)) || !Number.isInteger(Number(stopLoss))) {
        alert('Proszę wprowadzić prawidłowe wartości całkowite dla Take profit i Stop loss.');
        return;
    }

    const reader1 = new FileReader();
    const reader2 = new FileReader();

    reader1.onload = function(event) {
        const positionsFileContent = event.target.result;

        reader2.onload = function(event) {
            const pricesFileContent = event.target.result;

            eel.execute_backtest(positionsFile.name, positionsFileContent, pricesFile.name, pricesFileContent, takeProfit, stopLoss, outputName)(function(logMessage) {
                updateLog(logMessage);
            });
        };
        reader2.readAsDataURL(pricesFile);
    };
    reader1.readAsDataURL(positionsFile);
}

function updateLog(logMessage) {
    const logOutput = document.getElementById('logOutput');
    const newLogEntry = document.createElement('p');
    newLogEntry.innerHTML = logMessage.replace(/\n/g, '</p><p>');
    logOutput.appendChild(newLogEntry);
    alert('Backtest został wykonany. Sprawdź logi.');
}
