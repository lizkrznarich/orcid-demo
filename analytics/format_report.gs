//Live code at https://script.google.com/a/macros/orcid.org/d/MW2mm7bNZq99iVoxVyMqLB29EiE-8kxK_/edit?uiv=2&mid=ACjPJvHjd4pNA0NMT2IZ2uFP41W0d4vRUDFhMgUcFoJs0lYmdyLLqwsUxrep9A0_akuLA3KNefXrKmmpMWmrHjSfthrh3Gl34zCyrQI_5orldwojtXsc1pKMbqOox2wFOMxBl8WBnytZqgY

function getRawDataFilesList(){
  
  //get current report spreadsheet ID
  var report_ss = SpreadsheetApp.getActiveSpreadsheet();
  var report_ss_id = report_ss.getId();
  
  //get raw data folder
  var dataFolder = DriveApp.getFileById(report_ss_id).getParents().next().getFoldersByName('raw_data').next();
  
  //get raw data files
  var dataFiles = dataFolder.getFiles();
  
  return dataFiles;
}

function openLatestGaStats(){
  
  //create arrays and objects to hold file dates
  var arryGaFileDates = [];
  var objGaFilesByDate = {};
 
  //get raw data files list
  var dataFiles = getRawDataFilesList();
  
  //iterate through raw data files list
  while (dataFiles.hasNext()){
    
    var dataFile = dataFiles.next();
    var fileName = dataFile.getName();
    var fileDate = dataFile.getLastUpdated();
    
    //if file is ga_stats add to array
    if (fileName.indexOf("ga_stats") > -1){
      objGaFilesByDate[fileDate] = dataFile.getId();
      arryGaFileDates.push(dataFile.getLastUpdated());
    }
  }
  
  //find newest ga_stats file
  arryGaFileDates.sort(function(a,b){return b-a});
  var newestGaDate = arryGaFileDates[0];
  var newestGaFileID = objGaFilesByDate[newestGaDate];
  
  //open newest ga_stats file
  if (typeof newestGaFileID !== 'undefined') {
    var ga_ss = SpreadsheetApp.openById(newestGaFileID);
    //define sheet to pull ga data from
    var ga_sheet = ga_ss.getSheets()[0];
  }
  
  return ga_sheet;
 
 }

function openLatestOdStats(){
  
  //create arrays and objects to hold file dates
  var arryOdFileDates = [];
  var objOdFilesByDate = {};
  
  //get raw data files list
  var dataFiles = getRawDataFilesList();
  
  //iterate through raw data files list
  while (dataFiles.hasNext()){
    
    var dataFile = dataFiles.next();
    var fileName = dataFile.getName();
    var fileDate = dataFile.getLastUpdated();
    
    //if file is od_stats add to array
    if (fileName.indexOf("od_stats") > -1){
      objOdFilesByDate[fileDate] = dataFile.getId();
      arryOdFileDates.push(dataFile.getLastUpdated());
    }
  }

  //find newest od_stats file
  arryOdFileDates.sort(function(a,b){return b-a});
  var newestOdDate = arryOdFileDates[0];
  var newestOdFileID = objOdFilesByDate[newestOdDate];
  
  //open newest od_stats file
  if (typeof newestOdFileID !== 'undefined') {
    var od_ss = SpreadsheetApp.openById(newestOdFileID);
    //define sheet to pull od data from
    var od_sheet = od_ss.getSheets()[0];
  }
  
  return od_sheet;
 }


function formatReportDashboard(){

  //define report dashboard sheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var dashboard_sheet = ss.getSheets()[0];

  //define the stats sheets to get data from
  var ga_sheet = openLatestGaStats();
  var od_sheet = openLatestOdStats();

  //turns out that apps script can't create charts from data in another file
  //create new sheet to hold chart data then hide it
  ss.insertSheet(1);
  var chart_data_sheet = ss.getSheets()[1];
  chart_data_sheet.hideSheet();
    
  //styles
  var orcid_gray = '#808285';
  var orcid_blue = '#428BCA';
  var orcid_green = '#A6CE39';
  
  //apps script doesn't have any way to add styles systematically
  //hack using functions that add styles
  function h1_style(text_to_format){
    var formatted_text = text_to_format.setFontColor(orcid_gray).setFontSize(18).setFontWeight("bold").setFontStyle("normal");
    return formatted_text;
  }

  function h2_style(text_to_format){
    var formatted_text = text_to_format.setFontColor(orcid_gray).setFontSize(12).setFontWeight("normal").setFontStyle("italic");
    return formatted_text;
  }

  function h3_style(text_to_format){
    var formatted_text = text_to_format.setFontColor(orcid_blue).setFontSize(10).setFontWeight("bold").setFontStyle("normal").setBorder(false, false, true, false, false, false, orcid_gray, null);
    return formatted_text;
  }

  function h4_style(text_to_format){
    var formatted_text = text_to_format.setFontColor(orcid_gray).setFontSize(10).setFontWeight("bold").setFontStyle("normal");
    return formatted_text;
  }

  function body_style(text_to_format){
    var formatted_text = text_to_format.setFontColor(orcid_gray).setFontSize(10).setFontWeight("normal").setFontStyle("italic");
    return formatted_text;
  }

  //Sheet title
   var ga_group_name = ga_sheet.getRange("B2").getValue();
   var title = h1_style(dashboard_sheet.getRange("A1").setValue(ga_group_name));
   
  //Report dates  
   var ga_start_date = ga_sheet.getRange("B4").getValue().toDateString();
   var ga_end_date = ga_sheet.getRange("B5").getValue().toDateString();
   var report_dates = body_style(dashboard_sheet.getRange("A2").setValue(ga_start_date + " to " + ga_end_date));
   
  //Registry stats subtitle
   var reg_stats_subtitle = h2_style(dashboard_sheet.getRange("A3").setValue('Registry Statistics (Total across all time periods)'));


  //Creation/claim heading
  var creation_claim_heading = h3_style(dashboard_sheet.getRange("A5:G5").setValues([
     ["Record Creation/Claim Rate","","","","","",""]
    ]));

  //Creation/claim help text
   var creation_claim_help_text = body_style(dashboard_sheet.getRange("A6").setValue('Data about records created via the ORCID API using your client ID'));
  
  //Creation/claim data heading
  var creation_claim_data_heading = h4_style(dashboard_sheet.getRange("A7:D7").setValues([
     ["Created", "Claimed", "Unclaimed", "Claim Rate"]
   ]));
  
  //Creation/claim data
  //data from od_sheet goes here
    
  //Affiliation heading
  var affiliation_heading = h3_style(dashboard_sheet.getRange("A10:G10").setValues([
     ["Record Affiliation Counts","","","","","",""]
    ]));

  //Affiliation help text
  var affiliation_help_text = body_style(dashboard_sheet.getRange("A11").setValue('Data about records created via any method that include an affiliation with your organization'));

  //Email data heading
  var email_data_heading = h4_style(dashboard_sheet.getRange("A13").setValue('Email domain'));

  //Email help text
  var email_help_text = body_style(dashboard_sheet.getRange("A14").setValue("Records registered to an address in your organization's email domain"));

  //Email data
  //data from od_sheet goes here
  
  //Affiliation data heading
  var affiliation_data_heading = h4_style(dashboard_sheet.getRange("A17").setValue('Affiliation'));

  //Affiliation help text
  var affiliation_help_text = body_style(dashboard_sheet.getRange("A18").setValue('Records listing a past or present affiliation with your organization in the Education or Employment sections'));
  
  //Affiliation data
  //data from od_sheet goes here

  //Active affiliation data heading
  var active_affiliation_data_heading = h4_style(dashboard_sheet.getRange("A21").setValue('Active Affiliation'));

  //Active affiliation help text
  var active_affiliation_help_text = body_style(dashboard_sheet.getRange("A22").setValue('Records listing a current affiliation with your organization in the Education or Employment sections (current = no end date included)'));
    
  //Active affiliation data
  //data from od_sheet goes here
  
  //Integration analytics subtitle
   var analytics_subtitle = h2_style(dashboard_sheet.getRange("A26").setValue('Integration Analytics (Last 30 days)'));

  //Total new registrations heading 
  var new_reg_heading = h3_style(dashboard_sheet.getRange("A28:G28").setValues( [
     ["Total New Registrations","","","","","",""]
    ]));

  //Total new registrations help text
  var new_reg_help_text = body_style(dashboard_sheet.getRange("A29").setValue('Some help text here'));

  //Total new registrations values
  var ga_total_new_registrations = ga_sheet.getRange("B6").getValue();
  var total_new_registrations = dashboard_sheet.getRange("A30").setValue(ga_total_new_registrations);

  //Total integration users heading 
  var int_users_heading = h3_style(dashboard_sheet.getRange("A32:G32").setValues([
     ["Total Integration Users","","","","","",""]
    ]));

  //Total integration users help text
  var int_users_help_text = body_style(dashboard_sheet.getRange("A33").setValue('Some help text here'));

  //Total integration users values
  var ga_total_integration_users = ga_sheet.getRange("B7").getValue();
  var total_total_integration_users = dashboard_sheet.getRange("A34").setValue(ga_total_integration_users);

  //Total integration events heading 
  var int_events_heading = h3_style(dashboard_sheet.getRange("A36:G36").setValues([
     ["Total Integration Events","","","","","",""]
    ]));

  //Total integration events help text
  var int_events_help_text = body_style(dashboard_sheet.getRange("A37").setValue('Some help text here'));

  //Actions taken by users heading 
  var actions_by_users_heading = h3_style(dashboard_sheet.getRange("A49:G49").setValues([
     ["Actions Taken by Users","","","","","",""]
    ]));

  //Actions taken by users help text
  var actions_by_users_help_text = body_style(dashboard_sheet.getRange("A50").setValue('Some help text here'));

  //Users by country heading 
  var users_by_country_heading = h3_style(dashboard_sheet.getRange("A58:G58").setValues([
     ["Users by Country","","","","","",""]
    ]));

  //Users by country help text
  var users_by_country_help_text = body_style(dashboard_sheet.getRange("A59").setValue('Some help text here'));
  body_style(users_by_country_help_text);
  
  //Charts
  var totalEventsChart = createTotalEventsChart(ss, dashboard_sheet, chart_data_sheet, ga_sheet);
  var actionsTakenByUsersChart = createActionsTakenByUsersChart(ss, dashboard_sheet, chart_data_sheet, ga_sheet);
  var usersByCountryChart = createUsersByCountryChart(ss, dashboard_sheet, chart_data_sheet, ga_sheet);
}

function createTotalEventsChart(ss, dashboard_sheet, chart_data_sheet, ga_sheet) {
  var ga_chart_data = ga_sheet.getRange("A10:B40").getValues();
  var chart_data = chart_data_sheet.getRange("A10:B40").setValues(ga_chart_data);
  
  var chart = dashboard_sheet.newChart()
     .setChartType(Charts.ChartType.LINE)
     .addRange(chart_data_sheet.getRange('A10:B40'))
     .setPosition(38, 1, 7, 0)
     .build();
  dashboard_sheet.insertChart(chart);
}

function createActionsTakenByUsersChart(ss, dashboard_sheet, chart_data_sheet, ga_sheet) {
  var ga_chart_data = ga_sheet.getRange("A44:C48").getValues();
  var chart_data = chart_data_sheet.getRange("A44:C48").setValues(ga_chart_data);
  
  var chart = dashboard_sheet.newChart()
     .setChartType(Charts.ChartType.TABLE)
     .addRange(chart_data_sheet.getRange('A44:C48'))
     .setPosition(51, 1, 7, 0)
     .build();
  dashboard_sheet.insertChart(chart);
}

function createUsersByCountryChart(ss, dashboard_sheet, chart_data_sheet, ga_sheet) {
  var ga_chart_data = ga_sheet.getRange("A51:B71").getValues();
  var chart_data = chart_data_sheet.getRange("A51:B71").setValues(ga_chart_data);
  
  var chart = dashboard_sheet.newChart()
     .setChartType(Charts.ChartType.TABLE)
     .addRange(chart_data_sheet.getRange('A51:B71'))
     .setPosition(60, 1, 7, 0)
     .build();
  dashboard_sheet.insertChart(chart);
}
