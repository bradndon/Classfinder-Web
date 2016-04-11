//Copyright (C) Brandon Fox 2016
var classApp = angular.module('classApp', ['infinite-scroll']);
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
    $scope.showTitle[subject] = true;
    return true;
  }
  $scope.showSchedule = function(who) {
    if ($("#schedBtn").hasClass('schedule--selected')){
        $("#schedBtn").toggleClass('schedule--selected');
        $('#schedNum').css("display", "flex");
        $('.schedule__list').first().css("display","none");
        $('.schedule').first().css("overflow-y","");
        $('body').css("overflow-y","auto");
        $('.asdf').remove();
    } else {
      $("#schedBtn").toggleClass('schedule--selected');
      $('#schedNum').css("display", "none");
      $('.schedule__list').first().css("display","block");
      $('.schedule').first().css("overflow-y","auto");
      $('body').css("overflow-y","hidden");

      $scope.selectedClasses.forEach(function(x){
        console.log(x);
        x.day.forEach(function(y){
          var findSpot = function(time) {
            var t = time;
            var part = t%10;
            t/=10;
            part += t%10*10;
            console.log(part);
            console.log();
            return (56+62*(Math.floor(time/100)-5)+62*part/60.0);
          }
          findSpot(x.beginTime);
          findSpot(x.endTime);
          var doo = ["M","T","W","R","F","S","U"];
          var $newClass = $('<div style="background-color:white;opacity:.8;position:absolute;top:50px">asdf</div>');
          $newClass.addClass("asdf");
          $newClass.css("color","black");
          $newClass.css("top", findSpot(x.beginTime)+"px");
          // $newClass.css("margin","0 10px");
          $newClass.css("width",(window.innerWidth*.95)/7.0);
          $newClass.css("left", 11+(window.innerWidth*.95)/7.0*doo.indexOf(y));
          $newClass.css("height", findSpot(x.endTime)-findSpot(x.beginTime)+"px");
          $('.schedule__list').first().append($newClass);
        })

      });
    }
  }
  $scope.removeClass = function(index) {
    var id = $scope.selectedClasses[index]["id"];
    $('#UNIQUELABEL' + id + "_1").css("background-color","#385E0F");
    $('#'+id+'sign').text("+");
    $('#'+id+'text').text("Add to Schedule");
    $scope.selectedClasses.splice(index,1);
    $scope.$apply();
  }
  $scope.increaseClass = function(currClass,id) {
    currClass["id"] = id;
    var index = $scope.selectedClasses.indexOf(currClass)
    if(index > -1) {
      $scope.selectedClasses.splice(index,1);
      $('#UNIQUELABEL' + id + "_1").css("background-color","#385E0F");
      $('#'+id+'sign').text("+");
      $('#'+id+'text').text("Add to Schedule");
    } else {
      currClass["id"] = id
      $scope.selectedClasses.push(currClass);
      $('#UNIQUELABEL' + id + "_1").css("background-color","#c40806");
      $('#'+id+'sign').text("-");
      $('#'+id+'text').text("Remove from Schedule");
    }
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
