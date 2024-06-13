function executeBacktest() {
    const positionsFile = document.getElementById('positionsFile').files[0];
    const pricesFile = document.getElementById('pricesFile').files[0];
    const takeProfit = document.getElementById('takeProfit').value;
    const stopLoss = document.getElementById('stopLoss').value;
    const outputName = document.getElementById('outputName').value;
    const numberOfPips = document.getElementById('numberOfPips').value;
    const invert = document.getElementById('invert').checked;



    if (!positionsFile || !pricesFile) {
        alert('Please select both files.');
        return;
    }

    if (!takeProfit || !stopLoss || !numberOfPips) {
        alert('Please enter values for take profit, stop loss and number of pips');
        return;
    }

    if (!Number.isInteger(Number(takeProfit)) || !Number.isInteger(Number(stopLoss)) || !Number.isInteger(Number(numberOfPips))) {
        alert('Please enter valid integer values for take profit, stop loss and number of pips');
        return;
    }

    const reader1 = new FileReader();
    const reader2 = new FileReader();

    reader1.onload = function(event) {
        const positionsFileContent = event.target.result;

        reader2.onload = function(event) {
            const pricesFileContent = event.target.result;

            eel.execute_backtest(positionsFile.name, positionsFileContent, pricesFile.name, pricesFileContent, takeProfit, stopLoss, numberOfPips, invert)(function(logMessage) {
                updateLog(logMessage);
            });
        };
        reader2.readAsDataURL(pricesFile);
    };
    reader1.readAsDataURL(positionsFile);
}

document.getElementById('positionsFile').addEventListener('change', function() {
    const fileInput = this;
    const fileLabel = document.getElementById('first_file');
    if (fileInput.files.length > 0) {
        fileLabel.textContent = `${fileInput.files[0].name}`;
    } else {
        fileLabel.textContent = 'Choose file';
    }
});

document.getElementById('pricesFile').addEventListener('change', function() {
    const fileInput = this;
    const fileLabel = document.getElementById('second_file');
    if (fileInput.files.length > 0) {
        fileLabel.textContent = `${fileInput.files[0].name}`;
    } else {
        fileLabel.textContent = 'Choose file';
    }
});

eel.expose(updateLog);
function updateLog(logMessage) {
    const logOutput = document.getElementById('logOutput');
    logOutput.value += logMessage + '\n';
    logOutput.scrollTop = logOutput.scrollHeight;
}

eel.expose(setOutput);
function setOutput(content) {
    document.getElementById('outputSection').value = content;
}

eel.expose(block_output_name);
function block_output_name() {
    const outputName = document.getElementById('outputName');
    outputName.setAttribute('readonly', true);
    outputName.style.backgroundColor = '#444';
    outputName.style.cursor = 'not-allowed';
    outputName.value = '';
    outputName.placeholder = 'The backtest has not finished yet';
    block_save_button()
}

eel.expose(unlock_output_name);
function unlock_output_name() {
    const outputName = document.getElementById('outputName');
    outputName.removeAttribute('readonly');
    outputName.style.backgroundColor = '#333';
    outputName.style.cursor = 'text';
    outputName.placeholder = 'Enter name to save as PDF';
    unblock_save_button()
}

function unblock_save_button()
{
    const saveButton = document.getElementById('save');
    saveButton.removeAttribute('disabled');
    saveButton.style.cursor = 'pointer';
    saveButton.style.backgroundColor = 'green'; // Zmień kolor na zielony lub inny kolor wskazujący na aktywność
}

function block_save_button()
{
    const saveButton = document.getElementById('save');
    saveButton.setAttribute('disabled', true);
    saveButton.style.cursor = 'not-allowed';
    saveButton.style.backgroundColor = 'red'; // Zmień kolor na czerwony lub inny kolor wskazujący na brak aktywności
}



function changeText() {
    const label = document.getElementById('invert-text');
    if (invert.checked) {
        label.textContent = 'YES';
    } else {
        label.textContent = 'NO';
    }
}
eel.expose(createSampleChart);
function createSampleChart(PNL, positions) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const PNLlist = PNL;
    const positionslist = positions;
    const labels = PNLlist.map((_, index) => `${index + 1}`);
    const Yzeros = new Array(PNLlist.length).fill(0);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'PNL',
                    data: PNLlist,
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 2,
                    fill: false,
                },
                {
                    label: 'Position PNL',
                    data: positionslist,
                    borderColor: 'rgba(0, 0, 255, 1)',
                    borderWidth: 2,
                    fill: false,
                },
                {
                    label: 'Yzeros',
                    data: Yzeros,
                    borderColor: 'rgba(255, 255, 0, 1)',
                    borderWidth: 3,
                    fill: false,
                }
            ]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Position'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'PNL'
                    }
                }
            }
        }
    });
}


function printSections() {
    const outputSection = document.getElementById('outputSection').value;
    const outputName = document.getElementById('outputName').value || 'output'; // Domyślna nazwa, jeśli pole jest puste

    // Dodawanie nowej strony i zawartości outputSection
    const pdf = new jspdf.jsPDF();
    pdf.text("Output Section:", 10, 10);
    const outputLines = pdf.splitTextToSize(outputSection, 180);
    pdf.text(outputLines, 10, 20);

    // Zapis PDF z nazwą pobraną z elementu outputName
    pdf.save(`${outputName}.pdf`);
}
