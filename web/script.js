function executeBacktest() {
    const positionsFile = document.getElementById('positionsFile').files[0];
    const pricesFile = document.getElementById('pricesFile').files[0];
    const takeProfit = document.getElementById('takeProfit').value;
    const stopLoss = document.getElementById('stopLoss').value;
    const outputName = document.getElementById('outputName').value;

    if (!positionsFile || !pricesFile) {
        alert('Please select both files.');
        return;
    }

    if (!takeProfit || !stopLoss) {
        alert('Please enter values for Take profit, Stop loss');
        return;
    }

    if (!Number.isInteger(Number(takeProfit)) || !Number.isInteger(Number(stopLoss))) {
        alert('Please enter valid integer values for Take profit and Stop loss.');
        return;
    }

    const reader1 = new FileReader();
    const reader2 = new FileReader();

    reader1.onload = function(event) {
        const positionsFileContent = event.target.result;

        reader2.onload = function(event) {
            const pricesFileContent = event.target.result;

            eel.execute_backtest(positionsFile.name, positionsFileContent, pricesFile.name, pricesFileContent, takeProfit, stopLoss)(function(logMessage) {
                updateLog(logMessage);
            });
        };
        reader2.readAsDataURL(pricesFile);
    };
    reader1.readAsDataURL(positionsFile);
}

eel.expose(updateLog);
function updateLog(logMessage) {
    const logOutput = document.getElementById('logOutput');
    const newLogEntry = document.createElement('p');
    newLogEntry.innerHTML = logMessage.replace(/\n/g, '</p><p>');
    logOutput.appendChild(newLogEntry);
    logOutput.scrollTop = logOutput.scrollHeight;
}

eel.expose(block_output_name);
function block_output_name() {
    const outputName = document.getElementById('outputName');
    outputName.setAttribute('readonly', true);
    outputName.style.backgroundColor = '#444';
    outputName.style.cursor = 'not-allowed';
    outputName.value = '';
    outputName.placeholder = 'The backtest has not finished yet';
}

eel.expose(unlock_output_name);
function unlock_output_name() {
    const outputName = document.getElementById('outputName');
    outputName.removeAttribute('readonly');
    outputName.style.backgroundColor = '#333';
    outputName.style.cursor = 'text';
    outputName.placeholder = 'Enter name to save as PDF';
}



