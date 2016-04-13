//Copyright (C) Brandon Fox 2016
var classApp = angular.module('classApp', ['infinite-scroll','ngSanitize']);
classApp.controller('HomeCtrl', function($scope, $rootScope) {
  $scope.loaded = true;
  $scope.begin = 0;
  $scope.end = 2500;
  $scope.open = false;
  $scope.showTitle = {};
  $scope.exclusive = true;
  $scope.atLeast = true;
  $scope.courseNum = "";
  $scope.selectedClasses = [];
  $scope.subData = [];
  $scope.credits = 0;
  $scope.ruleset = {
    "class": [],
    gur: [],
    day: [],
    time: [],
    open: "",
    crenum: "0"
  };

  $scope.$watch('atLeast', function(newValue, oldValue) {$scope.reset()});
  $scope.$watch('exclusive', function(newValue, oldValue) {$scope.reset()});
  $scope.$watch('begin', function(newValue, oldValue) {$scope.reset()});
  $scope.$watch('end', function(newValue, oldValue) {$scope.reset()});
  $scope.$watch('courseNum', function(newValue, oldValue) {$scope.reset()});
  $scope.$watch('ruleset.open', function(newValue, oldValue) {$scope.reset()});
  $scope.$watch('ruleset.crenum', function(newValue, oldValue) {$scope.reset()});
  $scope.addMoreClasses = function() {
    if (!$scope.loaded && $scope.currSubject < $scope.subData.length) {
      var j = 0;
      var currSubText = $scope.subData[$scope.currSubject].text;
      for (var i = 0; i < 15; i++) {
        if ($scope.numShown + i + j >= $scope.allData[currSubText].length) {
          $scope.currSubject++;
          currSubText = $scope.subData[$scope.currSubject].text;
          while ($scope.allData[currSubText] == null) {
            $scope.currSubject++;
            currSubText = $scope.subData[$scope.currSubject].text;
          }
          currSubText = $scope.subData[$scope.currSubject].text;
          $scope.data[currSubText] = [];
          i = 0;
          j = 0;
          $scope.numShown = 0;
        }
        if ($scope.filter(currSubText, $scope.allData[currSubText][$scope.numShown + i + j])) {
          $scope.data[currSubText].push($scope.allData[currSubText][$scope.numShown + i + j]);
        } else {
          i--;
          j++;
        }
      }
      $scope.numShown += i + j;
    }
  }
  $scope.$on('list:filtered', $scope.addMoreClasses);

  $scope.filter = function(subject, currClass) {
    if (currClass.day == undefined) {
      currClass.add = "+"
      currClass.color = "#385E0F"
      currClass.text = "Add to Schedule";
    }
    var days = [];
    var day1 = currClass.time1.split(" ")[0];
    var day2 = "";
    if ($scope.courseNum != currClass.courseNum.substring(0, $scope.courseNum.length)) {
      return false;
    }
    if (currClass.time2 != null) {
      day2 = currClass.time2.split(" ")[0];
    }
    if (day1 != "TBA") {
      days = days.concat(day1.split(""));
    }
    if (day2 != "TBA" && day2 != "") {
      days = days.concat(day2.split(""));
    }
    var index = 0;
    currClass.day = days.sort();
    var returns = Array.apply(null, Array(6)).map(String.prototype.valueOf, "false");
    for (var rule in $scope.ruleset) {
      if ($scope.ruleset[rule].length == 0) {
        returns[index] = true;
      }
      if (rule == "day" && $scope.ruleset[rule].length != 0) {
        if ($scope.exclusive) {
          var is_same = ($scope.ruleset[rule].length == currClass[rule].length) && $scope.ruleset[rule].every(function(element, index) {
            return element === currClass[rule][index];
          });
          if (is_same) {
            returns[index] = true;
          } else {
            return false;
          }
        } else {
          for (var x in $scope.ruleset[rule]) {
            if ($scope.ruleset[rule].length != 0 && currClass[rule] == null || (currClass[rule] != null && currClass[rule].indexOf($scope.ruleset[rule][x]) <= -1)) {
              return false
            }
          }
          returns[index] = true;
        }
      } else if (rule == "time" && ($scope.begin > 0 || $scope.end < 2500)) {
        if (currClass.beginTime >= $scope.begin && currClass.endTime <= $scope.end) {
          returns[index] = true;
        } else {
          return false;
        }
      } else if (rule == "crenum") {
        if ($scope.atLeast) {
          if (currClass.crenum.indexOf("-") <= -1) {
            if (parseInt(currClass.crenum) >= parseInt($scope.ruleset.crenum)) {
              returns[index] = true;
            } else {
              return false;
            }
          } else {
            var range = currClass.crenum.split("-");
            if (parseInt($scope.ruleset.crenum) >= parseInt(range[0]) && parseInt($scope.ruleset.crenum) <= parseInt(range[1])) {
              returns[index] = true;
            } else {
              return false;
            }
          }
        } else {
          if (currClass.crenum.indexOf("-") <= -1) {
            if (parseInt(currClass.crenum) == parseInt($scope.ruleset.crenum)) {
              returns[index] = true;
            } else {
              return false;
            }
          } else {
            return false;
          }
        }
      } else {
        if (typeof $scope.ruleset[rule] === 'object') {
          for (var x in $scope.ruleset[rule]) {

            if ($scope.ruleset[rule].length != 0 && currClass[rule] == null || (currClass[rule] != null && currClass[rule].indexOf($scope.ruleset[rule][x]) <= -1)) {} else {
              returns[index] = true;
            }
          }
        } else {
          if ($scope.ruleset[rule].length != 0 && currClass[rule] == null || (currClass[rule] != null && currClass[rule].indexOf($scope.ruleset[rule]) <= -1)) {} else {
            returns[index] = true;
          }
        }
        if (returns[index] == "false") {
          return false
        }

      }
      index++;
    }
    if ($scope.selectedClasses.indexOf(currClass)<=-1){
      if(!$scope.overlapsWithSchedule(currClass)) {
        currClass.add = "<i class='fa fa-ban'></i>";
        currClass.color = "#303030"
        currClass.text = "Overlaps with Schedule";
      } else {
        currClass.add = "<i class='fa fa-plus'></i>"
        currClass.color = "#385E0F"
        currClass.text = "Add to Schedule";
      }
    }
    $scope.showTitle[subject] = true;
    return  true;
  }
  $scope.showSidebar = function() {
    $(".sidebar").toggleClass("sidebar--show");
    $('.sidebar__svg').toggleClass("fa-pencil");
    $('.sidebar__svg').toggleClass("fa-times");
    $('.content').toggleClass("content--noflow");
  }
  $scope.showSchedule = function(who) {
    if ($("#schedBtn").hasClass('schedule--selected')){
        $('#schedNum').css("display", "flex");
        $('.schedule__list').first().css("display","none");
        $('.schedule').first().css("overflow-y","");
        $('.schedule__tab').remove();
    } else {
      $('#schedNum').css("display", "none");
      $('.schedule__list').first().css("display","block");
      $('.schedule').first().css("overflow-y","auto");
      $scope.createSchedule();
    }
    $("#schedBtn").toggleClass('schedule--selected');
    $('.schedule__svg').toggleClass("fa-calendar");
    $('.schedule__svg').toggleClass("fa-times");
    $('.content').toggleClass("content--noflowsmall");
  }
  $scope.createSchedule = function() {
    $('.schedule__tab').remove();
    $scope.credits = 0;
    var index = 0;
    $scope.selectedClasses.forEach(function(x){
      index++;
      if(index == 6) {
        index=1;
      }
      console.log(x);
      $scope.credits += parseInt(x.crenum);
      x.daytime.forEach(function(y){
        var findSpot = function(time) {
          var t = time;
          var part = t%10;
          t/=10;
          part += t%10*10;
          return (66+58*(Math.floor(time/100)-8)+58*part/60.0);
        }
        var dayList = ["M","T","W","R","F","S","U"];
        var $newClass = $('<div></div>');
        $newClass.html("<h4 class='schedule__classtitle'>"+ x.class + "</h4>");
        $newClass.addClass("schedule__tab");
        $newClass.addClass("color"+index);
        $newClass.css("top", findSpot(y[1])+"px");
        $newClass.css("right", 1+90/5.0*(4-dayList.indexOf(y[0]))+"%");
        $newClass.css("height", findSpot(y[2])-findSpot(y[1])+"px");
        $('.schedule__list').first().append($newClass);
      })

    });
  }
  $scope.removeClass = function(index) {
    var id = $scope.selectedClasses[index]["id"];
    $('#UNIQUELABEL' + $scope.selectedClasses[index]["crn"] + "_1").css("background-color","#385E0F");
    $('#'+$scope.selectedClasses[index]["crn"]+'sign').text("+");
    $('#'+$scope.selectedClasses[index]["crn"]+'text').text("Add to Schedule");
    $scope.selectedClasses.splice(index,1);
    $scope.$apply();
  }
  $scope.increaseClass = function(currClass) {
    var index = $scope.selectedClasses.indexOf(currClass)
    if(index > -1) {
      currClass.add= "<i class='fa fa-plus'></i>";
      $scope.selectedClasses.splice(index,1);
      currClass.color="#385E0F";
      currClass.text = "Add to Schedule"

    } else {
      if (currClass.text.indexOf("Overlaps") <= -1){
        $scope.selectedClasses.push(currClass);
        currClass.add= "<i class='fa fa-minus'></i>";
        currClass.color="#C40806";
        currClass.text = "Remove from Schedule"
      }
    }
    if ($("#schedBtn").hasClass('schedule--selected')){
      $scope.createSchedule();
    }
    $scope.reset();
  }
  $scope.overlapsWithSchedule = function(currClass) {
    var check = true;
    $scope.selectedClasses.forEach(function(c){
      c.daytime.forEach(function(y){
        currClass.daytime.forEach(function(x) {
            if (y[0] == x[0]) {
              if((y[1] <= x[1] && y[2]) >= x[1] || (y[1] <= x[2] && y[2] >= x[2])){
                check = false;
              }
            }
        })
      })
    })
    return check;
  }
  $scope.dayClicked = function(day) {
    var index = $scope.ruleset.day.indexOf(day)
    if (index > -1) {
      $scope.ruleset.day.splice(index, 1);
    } else {
      $scope.ruleset.day.push(day);
    }
    $scope.ruleset.day.sort();
    $scope.reset();
  }
  $.getJSON("js/rmpFixed.json", function(data) {
    $scope.scores = {};
    for (score in data) {
      $scope.scores[data[score].name] = data[score].rating;
    }
  });



  $.getJSON("http://sub.localhost:4568/menu.json", function(data) {
    $.getJSON("http://sub.localhost:4568/classes.json", function(data) {
      console.log(data);
      $scope.allData = data;
      $scope.loaded = false;
      $scope.$apply();
      $scope.reset();
    });
    $scope.menuData = data;
    $scope.subData = []
    var gurData = []
    for (obj in data.Subject) {
      $scope.subData.push({
        id: data.Subject[obj],
        text: obj
      });
      $scope.showTitle[obj] = false;
    }
    for (obj in data["GUR/Course Attribute"]) {
      gurData.push({
        id: data["GUR/Course Attribute"][obj],
        text: obj
      });
    }
    for (obj in data.Instructor)
      $scope.subData.sort(function(a, b) {
        return a.text.localeCompare(b.text);
      });
    gurData.sort(function(a, b) {
      return a.text.localeCompare(b.text);
    });
    $scope.subData.splice(4, 1);
    $('.subjectSelect').select2({
      data: $scope.subData
    });
    $('.subjectSelect').on("select2:select", function(e) {
      $scope.ruleset["class"].push(e.params.data.id);
      $scope.reset();
    });
    $('.subjectSelect').on("select2:unselect", function(e) {
      var i = $scope.ruleset["class"].indexOf(e.params.data.id);
      $scope.ruleset["class"].splice(i, 1);
      $scope.reset();
    });
    $('.gurSelect').select2({
      data: gurData
    });
    $('.gurSelect').on("select2:select", function(e) {
      $scope.ruleset.gur.push(e.params.data.id);
      $scope.reset();
    });
    $('.gurSelect').on("select2:unselect", function(e) {
      var i = $scope.ruleset.gur.indexOf(e.params.data.id);
      $scope.ruleset.gur.splice(i, 1);
      $scope.reset();
    });
    $scope.currSubject = 2;
    $scope.$apply();
  });
  $scope.reset = function() {
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
    $scope.data = {
      "Accounting": []
    };
    $scope.currSubject = 2;
    $scope.numShown = 0;
    $scope.$emit('list:filtered');

    $scope.$apply();
  }

});
