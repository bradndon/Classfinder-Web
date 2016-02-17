var classApp = angular.module('classApp', []);
classApp.controller('HomeCtrl', function($scope) {
  $scope.ruleset = {
    "class": [],
    gur: [],
    day: []
  };
  $scope.showTitle = {};
  $scope.exclusive = true;
  $scope.$watch('exclusive', function(newValue, oldValue) {
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
  });
  $scope.filter = function(subject, currClass) {
    var days = [];
    var day1 = currClass.time1.split(" ")[0];
    var day2 = "";
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
    var returns = Array.apply(null, Array(3)).map(String.prototype.valueOf, "false");
    for (var rule in $scope.ruleset) {
      if ($scope.ruleset[rule].length == 0) {
        returns[index] = true;
      }
      if (rule == "day" && $scope.exclusive && $scope.ruleset[rule].length != 0) {
        var is_same = ($scope.ruleset[rule].length == currClass[rule].length) && $scope.ruleset[rule].every(function(element, index) {
            return element === currClass[rule][index];
        });
        if (is_same){
          returns[index] = true;
        } else {
          return false;
        }
      } else {
        for (var x in $scope.ruleset[rule]) {
          if ($scope.ruleset[rule].length != 0 && currClass[rule] == null || (currClass[rule] != null && currClass[rule].indexOf($scope.ruleset[rule][x]) <= -1)) {} else {
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
  $scope.dayClicked = function(day) {
    var index = $scope.ruleset.day.indexOf(day)
    if (index > -1) {
      $scope.ruleset.day.splice(index, 1);
    } else {
      $scope.ruleset.day.push(day);
    }
    $scope.ruleset.day.sort();
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
  }
  $.getJSON("http://localhost:4568/v1/class/201610?apikey=mine", function(data) {
    $scope.allData = data;
    $scope.data = data;
    $scope.$apply();

  });
  $.getJSON("http://localhost:4568/v1/menu?apikey=mine", function(data) {
    $scope.menuData = data;
    var subData = []
    var gurData = []
    for (obj in data.Subject) {
      subData.push({
        id: data.Subject[obj],
        text: obj
      });
      $scope.showTitle[obj] = true;
    }
    for (obj in data["GUR/Course Attribute"]) {
      gurData.push({
        id: data["GUR/Course Attribute"][obj],
        text: obj
      });
    }
    for (obj in data.Instructor)
      subData.sort(function(a, b) {
        return a.text.localeCompare(b.text);
      });
    gurData.sort(function(a, b) {
      return a.text.localeCompare(b.text);
    });
    console.log($scope.menuData);
    $('.subjectSelect').select2({
      data: subData
    });
    $('.subjectSelect').on("select2:select", function(e) {
      $scope.ruleset["class"].push(e.params.data.id);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.$apply();
    });
    $('.subjectSelect').on("select2:unselect", function(e) {
      var i2 = $scope.ruleset["class"].indexOf(e.params.data.id);
      $scope.ruleset["class"].splice(i2, 1);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.$apply();
    });
    $('.gurSelect').select2({
      data: gurData
    });
    $('.gurSelect').on("select2:select", function(e) {
      $scope.ruleset.gur.push(e.params.data.id);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.$apply();
    });
    $('.gurSelect').on("select2:unselect", function(e) {
      var i2 = $scope.ruleset.gur.indexOf(e.params.data.id);
      $scope.ruleset.gur.splice(i2, 1);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.$apply();
    });
    $scope.$apply();
    console.log($scope.showTitle);
  });
});
