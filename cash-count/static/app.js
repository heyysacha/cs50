//changeable depending on business needs
const floatAmount = 200;

const hundredInput = document.getElementById("hundred-input");
const hundredTotal = document.getElementById("hundred-total");
const fiftyInput = document.getElementById("fifty-input");
const fiftyTotal = document.getElementById("fifty-total");
const twentyInput = document.getElementById("twenty-input");
const twentyTotal = document.getElementById("twenty-total");
const tenInput = document.getElementById("ten-input");
const tenTotal = document.getElementById("ten-total");
const fiveInput = document.getElementById("five-input");
const fiveTotal = document.getElementById("five-total");
const oneInput = document.getElementById("one-input");
const oneTotal = document.getElementById("one-total");
const quarterInput = document.getElementById("quarter-input");
const quarterTotal = document.getElementById("quarter-total");
const dimeInput = document.getElementById("dime-input");
const dimeTotal = document.getElementById("dime-total");
const nickelInput = document.getElementById("nickel-input");
const nickelTotal = document.getElementById("nickel-total");
const pennyInput = document.getElementById("penny-input");
const pennyTotal = document.getElementById("penny-total");
const total = document.getElementById("total");
const variance = document.getElementById("variance");
const expected = document.getElementById("expected");
const regSales = document.getElementById("reg-sales");

const totalsArr = [hundredTotal, fiftyTotal, twentyTotal, tenTotal, fiveTotal, oneTotal, quarterTotal, dimeTotal, nickelTotal, pennyTotal];
const inputsArr = [hundredInput, fiftyInput, twentyInput, tenInput, fiveInput, oneInput, quarterInput, dimeInput, nickelInput, pennyInput];
const amountsArr = [100, 50, 20, 10, 5, 1, 0.25, 0.1, 0.05, 0.01];

expected.value = floatAmount.toFixed(2);

regSales.addEventListener('change', () => {
    expected.value = (parseFloat(regSales.value) + parseFloat(floatAmount)).toFixed(2);
    varianceUpdate();
})

function totalCash() {
    let countTotal = 0;
    for (let i=0; i < totalsArr.length; i++)
        if (parseFloat(totalsArr[i].innerText))
        {
            countTotal+=parseFloat(totalsArr[i].innerText);
        }
    total.value = countTotal.toFixed(2);
};
totalCash();

function inputListeners() {
    for (let i=0; i < inputsArr.length; i++)
    {
        inputsArr[i].addEventListener('change', () => {
            totalsArr[i].innerText = (amountsArr[i]*inputsArr[i].value).toFixed(2);
            totalCash();
            varianceUpdate();
        })
    }
};
inputListeners();

function varianceUpdate() {
    let expectedTotal = parseFloat(expected.value);
    if ((parseFloat(total.value) - expectedTotal) !== 0)
    {
        if ((parseFloat(total.value) - expectedTotal) > 0)
        {
            variance.value = `+ ${(parseFloat(total.value) - expectedTotal).toFixed(2)}`
        }
        else
        {
            variance.value = (parseFloat(total.value) - expectedTotal).toFixed(2);
        }
        variance.style.color = 'red';
    }
    else
    {
        variance.value = (parseFloat(total.value) - expectedTotal).toFixed(2);
        variance.style.color = 'black';
    }
};
varianceUpdate();
