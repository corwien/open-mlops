export default{
    formatTime:function(row, column) { //日期格式化
        var date = row[column.property]; 
        if (date == undefined) {  
            return "";  
        }  
        return moment(date).format("YYYY-MM-DD HH:mm:ss");  
    }   
}
