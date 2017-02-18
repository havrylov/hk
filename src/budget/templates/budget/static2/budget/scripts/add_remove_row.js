/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

var rowNum = 0;
function addRow() {
    if (rowNum < 100) {
        rowNum++;
        var row = '<tr id="rowNum' + rowNum + '"><td><input autocomplete="on" placeholder="Date or empty for now" type="text" name="date" id="date" title="Date of the transaction"></td>';
        row = row + '<td><input autocomplete="on" placeholder="Purpose" type="text" name="purpose" id="purpose" title="Purpose or Source"></td>';
        row = row + '<td><input autocomplete="on" placeholder="Amount" type="number" step="0.01" name="amount" id="amount" title="Amount of the transaction"></td>';
//            row = row + '<textarea placeholder="comment" tabindex="' + (4 + 4 * rowNum) + '" style="height: 15px;" name="comment" id="comment" title="Free comment" rows="1" form="itemRows" maxlength="255" wrap="soft" cols="50"></textarea>';
        row = row + '<td><input  placeholder="comment" type="text" name="comment" id="comment" title="Free comment"></td>'
        row = row + '<td><input  type="button" name="add" id="add" value="+" class="addButton" onclick="addRow();">';
        row = row + '<td><input type="button" value="X" onclick="removeRow(' + rowNum + ');" class="addButton"></td></tr>';
        jQuery('#itemRows').append(row);
    }
}

function removeRow(rnum) {
    jQuery('#rowNum' + rnum).remove();
}



