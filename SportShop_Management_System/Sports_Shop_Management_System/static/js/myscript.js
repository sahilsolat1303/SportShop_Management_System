function decrement(mid)
{
//     alert("Decrement clicked!!!")
    txtQty = document.getElementById(mid);
    val = parseInt(txtQty.value);
    if (val>1)
    {
        val = val -1;
    }
    txtQty.value = val;
 }

function increment(mid)
{
   txtQty = document.getElementById(mid);
    val = parseInt(txtQty.value);
    if (val<5)
    {
        val = val + 1;
    }
    txtQty.value = val;
}