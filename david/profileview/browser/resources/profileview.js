var app = angular.module('app', ['ngResource', 'ngRoute']);


app.factory('ProfileFactory', ['$resource', function($resource){
  return function(query){
    return $resource('./@@profileview.json', {
      path: query.path,
      query: query.query,
      target: query.target,
      kwargs: query.kwargs
    });
  };
}]);


app.controller('ProfileController', ['$scope', '$location', 'ProfileFactory', function($scope, $location, ProfileFactory){

  $scope.profile = undefined;
  $scope.new_entry = '';
  $scope.path = '';
  $scope.query = [];

  $scope.params = undefined;

  var load_profile = function(callback){
    var query = {
      target: $location.search().target,
      kwargs: $location.search().kwargs,
      path: $scope.path,
      query: JSON.stringify($scope.query)
    };

    $scope.params = query;

    ProfileFactory(query).get(function(response){
      $scope.path = response.profile;
      $scope.profile = response.data;
      if (callback) callback(response);
    });

  };

  load_profile();

  var reload_profile = function(){
    load_profile(function(){
      document.getElementById('newentry').focus();
    });
  };

  $scope.clear_query = function(){
    $scope.query = [];
    reload_profile();
  };

  $scope.execute_query = function(){
    if ($scope.new_entry === 'clear'){
      $scope.new_entry = '';
      $scope.query = [];
      reload_profile();
    }

    if ($scope.new_entry !== ''){
      $scope.query[$scope.query.length] = $scope.new_entry;
      $scope.new_entry = '';
      reload_profile();
    }
  };

  $scope.on_enter = function($event){
    if($event.keyCode === 13){
      $scope.execute_query();
    }
  };

}]);
