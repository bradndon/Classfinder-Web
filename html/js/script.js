var classApp = angular.module('classApp', []);
classApp.controller('HomeCtrl', function($scope) {
  $scope.ruleset = {"class": [], gur: [], day: []};
  $scope.filter = function(currClass) {
    var index = 0;
    var returns = Array.apply(null, Array(2)).map(String.prototype.valueOf,"false");
    for (var rule in $scope.ruleset) {
      if ($scope.ruleset[rule].length == 0) {
        returns[index] = true;
      }
      for (var x in $scope.ruleset[rule]) {
        if ($scope.ruleset[rule].length != 0 && currClass[rule] == null || (currClass[rule] != null && currClass[rule].indexOf($scope.ruleset[rule][x]) <= -1)) {
        } else {
          returns[index] = true;
        }
      }
    index++;
    }
    if (returns.indexOf("false") > -1){
      return false;
    }
    return true;
  }
  $scope.dayClicked = function(day){
    var index = $scope.ruleset.day.indexOf(day)
    if (index > -1){
      $scope.ruleset.day.splice(index,1);
    } else {
      $scope.ruleset.day.push(day);
    }
    console.log($scope.ruleset.day);
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
    for (obj in data.Subject){
        subData.push({id: data.Subject[obj], text: obj});
    }
    for (obj in data["GUR/Course Attribute"]){
        gurData.push({id: data["GUR/Course Attribute"][obj], text: obj});
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
    $('.subjectSelect').on("select2:select", function (e) {
      $scope.selected.push(e.params.data.text);
      $scope.ruleset["class"].push(e.params.data.id);
      $scope.$apply();
    });
    $('.subjectSelect').on("select2:unselect", function (e) {
      var index = $scope.selected.indexOf(e.params.data.text)
      var i2 =    $scope.ruleset["class"].indexOf(e.params.data.id);

      $scope.selected.splice(index, 1);
      $scope.ruleset["class"].splice(i2, 1);
      $scope.$apply();
    });
    $('.gurSelect').select2({
      data: gurData
    });
    $('.gurSelect').on("select2:select", function (e) {
      $scope.selectedGur.push(e.params.data.id);
      $scope.ruleset.gur.push(e.params.data.id);
      $scope.$apply();
      console.log($scope.ruleset);
    });
    $('.gurSelect').on("select2:unselect", function (e) {
      var index = $scope.selectedGur.indexOf(e.params.data.id)
      var i2 =    $scope.ruleset.gur.indexOf(e.params.data.id);

      $scope.selectedGur.splice(index, 1);
      $scope.ruleset.gur.splice(i2, 1);
      $scope.$apply();
    });
    $scope.$apply();
  });
});
