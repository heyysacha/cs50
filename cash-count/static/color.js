const totalVar = document.getElementById('total-var');

if (parseFloat(totalVar.innerText.slice(1,-1)) != 0)
{
    if (parseFloat(totalVar.innerText.slice(1,-1)) > 0)
    {
        totalVar.style.color = 'green';
    }
    else
    {
        totalVar.style.color = 'red';
    }

}

const variances = document.getElementsByClassName('var');

for (let i=0; i < variances.length; i++)
{
    if (parseFloat(variances[i].innerText.slice(1,-1)) != 0)
    {
        console.log(variances[i].innerText.slice(1,-1))
        if (parseFloat(variances[i].innerText.slice(1,-1)) > 0)
            {
                variances[i].style.color = 'green';
            }
        else
            {
                variances[i].style.color = 'red';
            }
    }
}
