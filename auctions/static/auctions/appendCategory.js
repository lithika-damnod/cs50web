document.getElementById("cat-add-btn").addEventListener("click", function(){
    // get the name of new category 
    let catName = document.getElementById("cat-desc").value; 

    // create input element 
    var inpElem = document.createElement("input");   
    inpElem.classList.add("form-check-input"); 
    inpElem.setAttribute("type", "checkbox"); 
    inpElem.value = catName; 
    inpElem.setAttribute("id", "flexCheckDefault"); 
    inpElem.setAttribute("name", "cat"); 

    // create label element
    var labelElem = document.createElement("label"); 
    labelElem.classList.add("form-check-label"); 
    labelElem.setAttribute("for", "flexCheckDefault"); 
    labelElem.innerHTML = catName; 
    
    // append childs
    document.getElementsByClassName("form-check")[0].appendChild(inpElem); 
    document.getElementsByClassName("form-check")[0].appendChild(labelElem); 
    document.getElementsByClassName("form-check")[0].innerHTML += "<br>"; 

    // clear out what's already written in the input box
    document.getElementById("cat-desc").value=""; 
}); 