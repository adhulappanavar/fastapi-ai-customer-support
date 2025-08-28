console.log('Testing ticketing interface'); 
if (window.customerSupportUI) { 
    console.log('CustomerSupportUI exists'); 
    window.customerSupportUI.showTicketing(); 
} else { 
    console.log('CustomerSupportUI not found'); 
}
