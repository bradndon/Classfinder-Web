var classApp = angular.module('classApp', ['infinite-scroll']);
classApp.controller('HomeCtrl', function($scope, $rootScope) {
  $scope.loaded = true;
  $scope.begin = 0;
  $scope.end = 2500;
  $scope.ruleset = {
    "class": [],
    gur: [],
    day: [],
    time: []
  };
  $scope.showTitle = {};
  $scope.exclusive = true;
  $scope.courseNum = "";
  $scope.$watch('exclusive', function(newValue, oldValue) {
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
    $scope.data = {"Accounting":[]};
    $scope.currSubject = 2;
    $scope.numShown = 0;
    $scope.$emit('list:filtered')
  });
  $scope.$watch('begin', function(newValue, oldValue) {
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
    $scope.data = {"Accounting":[]};
    $scope.currSubject = 2;
    $scope.numShown = 0;
    $scope.$emit('list:filtered')
  });
  $scope.$watch('end', function(newValue, oldValue) {
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
    $scope.data = {"Accounting":[]};
    $scope.currSubject = 2;
    $scope.numShown = 0;
    $scope.$emit('list:filtered')
  });
  $scope.$on('list:filtered', function (event, data) {
  $scope.addMoreClasses();
});
  $scope.$watch('courseNum', function(newValue, oldValue) {
    for (obj in $scope.showTitle) {
      $scope.showTitle[obj] = false;
    }
    $scope.data = {"Accounting": []};
    $scope.currSubject = 2;
    $scope.numShown = 0;
    $scope.$emit('list:filtered');
  });
  $scope.addMoreClasses = function() {
    if (!$scope.loaded){
    var j = 0;
    for (var i = 0; i < 10; i ++) {
      if ($scope.numShown + i + j >= $scope.dataToShow[$scope.subData[$scope.currSubject].text].length){
        $scope.currSubject ++;
        while($scope.dataToShow[$scope.subData[$scope.currSubject].text] == null){
          $scope.currSubject++;
        }

        $scope.data[$scope.subData[$scope.currSubject].text] = [];
        i=0;
        $scope.numShown = 0;
        j=0;
      }
      if($scope.filter($scope.subData[$scope.currSubject].text, $scope.dataToShow[$scope.subData[$scope.currSubject].text][$scope.numShown+i+j])){
        $scope.data[$scope.subData[$scope.currSubject].text].push($scope.dataToShow[$scope.subData[$scope.currSubject].text][$scope.numShown+i+j]);
      } else {
        i--;
        j++;
      }
    }
    $scope.numShown += i+j;
  }
  }
  $scope.filter = function(subject, currClass) {
    var days = [];
    var day1 = currClass.time1.split(" ")[0];
    var day2 = "";
    if ($scope.courseNum != currClass.courseNum.substring(0,$scope.courseNum.length)){
      return false;
    }
    console.log(currClass.beginTime);
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
    var returns = Array.apply(null, Array(4)).map(String.prototype.valueOf, "false");
    for (var rule in $scope.ruleset) {
      if ($scope.ruleset[rule].length == 0) {
        returns[index] = true;
      }
      if (rule == "day" && $scope.ruleset[rule].length != 0) {
        if($scope.exclusive){
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
            if ($scope.ruleset[rule].length != 0 && currClass[rule] == null || (currClass[rule] != null && currClass[rule].indexOf($scope.ruleset[rule][x]) <= -1)) {
              return false
            }
          }
          returns[index] = true;
        }
      } else if(rule=="time" && ($scope.begin > 0 || $scope.end < 2500)){
          if (currClass.beginTime >= $scope.begin && currClass.endTime <= $scope.end){
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
    $scope.currSubject = 2;
    $scope.data = {"Accounting": []};
    $scope.numShown = 0;
    $scope.$emit('list:filtered')
  }
  $.getJSON("http://localhost:4568/v1/class/201620?apikey=mine", function(data) {
    $scope.allData = data;
    $scope.dataToShow = data;
    $scope.currSubject = 2;
    $scope.data = {"Accounting": []};
    $scope.numShown = 0;
    $scope.$emit('list:filtered')
    $scope.loaded = false;
    $scope.$apply();


  });
  $.getJSON("http://localhost:4568/v1/menu?apikey=mine", function(data) {
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
    $scope.subData.splice(4,1);
    $('.subjectSelect').select2({
      data: $scope.subData
    });
    $('.subjectSelect').on("select2:select", function(e) {
      $scope.ruleset["class"].push(e.params.data.id);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.currSubject = 2;
      $scope.data = {"Accounting": []};
      $scope.numShown = 0;
      $scope.$emit('list:filtered')
      $scope.$apply();
    });
    $('.subjectSelect').on("select2:unselect", function(e) {
      var i2 = $scope.ruleset["class"].indexOf(e.params.data.id);
      $scope.ruleset["class"].splice(i2, 1);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.currSubject = 2;
      $scope.data = {"Accounting": []};
      $scope.numShown = 0;
      $scope.$emit('list:filtered')
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
      $scope.currSubject = 2;
      $scope.data = {"Accounting": []};
      $scope.numShown = 0;
      $scope.$emit('list:filtered')
      $scope.$apply();
    });
    $('.gurSelect').on("select2:unselect", function(e) {
      var i2 = $scope.ruleset.gur.indexOf(e.params.data.id);
      $scope.ruleset.gur.splice(i2, 1);
      for (obj in $scope.showTitle) {
        $scope.showTitle[obj] = false;
      }
      $scope.currSubject = 2;
      $scope.data = {"Accounting": []};
      $scope.numShown = 0;
      $scope.$emit('list:filtered')
      $scope.$apply();
    });
    $scope.currSubject = 2;

    $scope.$apply();
  });
});
