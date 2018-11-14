function header_selection_update() {

    const header_select = document.getElementById("form_control_headers_select");
    const selected_header = header_select.options[header_select.selectedIndex].innerHTML;

    const types_string = document.getElementById("header_types_string").innerHTML;
    const types_string_json = types_string.replace(/'/g, "\"");
    const types_object = JSON.parse(types_string_json);

    const selected_type = types_object[selected_header];
    document.getElementById("type_hidden").value = selected_type;

    const type_specific_forms = document.getElementsByClassName("type_specific_form");
    for (var i = 0; i < type_specific_forms.length; i++) {
        type_specific_forms[i].style.display = 'none'
    }

    document.getElementById('type_specific_form_' + selected_type).style.display = ''
}

window.onload = () => {

    header_selection_update();
    document.getElementById('form_control_headers_select').onchange = function () {
        header_selection_update();
    };

};