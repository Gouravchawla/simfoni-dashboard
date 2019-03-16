angular.module("app", ["highcharts-ng", "daterangepicker", "app.config"])
    .config(['$interpolateProvider', '$compileProvider', function($interpolateProvider, $compileProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $compileProvider.debugInfoEnabled(false);
    }])
    .controller('DashboardCtrl', ['$scope', 'dashboardService', 'SERVER_CONFIG', function ($scope, dashboardService, SERVER_CONFIG) {

      $scope.buyers = SERVER_CONFIG.INITIAL_DATA.buyers;
      $scope.departments = SERVER_CONFIG.INITIAL_DATA.departments;
      $scope.members = SERVER_CONFIG.INITIAL_DATA.members;
      $scope.dateRangePicker = {
        date: {
          startDate: moment(SERVER_CONFIG.INITIAL_DATA.start_date, 'YYYY-MM-DD'),
          endDate: moment(SERVER_CONFIG.INITIAL_DATA.end_date, 'YYYY-MM-DD')
        },
        options: {
          showDropdowns: true,
          ranges: {
            'Today': [moment(), moment()],
            'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Last 7 Days': [moment().subtract(6, 'days'), moment()],
            'Last 30 Days': [moment().subtract(29, 'days'), moment()],
            'Last 6 Months': [moment().subtract(180, 'days'), moment()],
            'Last 1 Year': [moment().subtract(365, 'days'), moment()],
          },
          locale: {
            applyLabel: "Apply",
            cancelLabel: 'Cancel',
            customRangeLabel: 'Custom range',
            separator: ' to ',
            // format: "YYYY-MM-DD", //will give you 2017-01-06
            format: "MMM D, YYYY", //will give you 6-Jan-17
            //format: "D-MMMM-YY", //will give you 6-January-17
        },
          eventHandlers: {
            'apply.daterangepicker': function(event, picker) {
              console.log("Applied ", event, picker, $scope.dateRangePicker.date);
              params.startDate = $scope.dateRangePicker.date.startDate;
              params.endDate = $scope.dateRangePicker.date.endDate;
              dashboardService.getFilteredData(params).then(function(response) {
                console.log("Response: ", response);
                $scope.charts = response.data.data.default_charts;
                $scope.buyers = response.data.data.buyers;
                $scope.departments = response.data.data.departments;
                $scope.members = response.data.data.members;
              });
            }
          },
          opens: "left"
        }
      };
      $scope.charts = SERVER_CONFIG.INITIAL_DATA.default_charts;

      $scope.selectedBuyer = 'Buyer';
      $scope.setSelectedBuyer = setSelectedBuyer;
      $scope.selectedDepartment = 'Department';
      $scope.setSelectedDepartment = setSelectedDepartment;
      $scope.selectedMember = 'Team member';
      $scope.setSelectedMember = setSelectedMember;
      var params = {};

      ///
      function setSelectedBuyer(buyer) {
        $scope.selectedBuyer = buyer;
        params.buyer = buyer;

        dashboardService.getFilteredData(params).then(function(response) {
          console.log("Response: ", response);
          $scope.charts = response.data.data.default_charts;
          $scope.buyers = response.data.data.buyers;
          $scope.departments = response.data.data.departments;
          $scope.members = response.data.data.members;
        });
      }

      function setSelectedDepartment(department) {
        $scope.selectedDepartment = department;
        params.department = department;

        dashboardService.getFilteredData(params).then(function(response) {
          console.log("Response: ", response);
          $scope.charts = response.data.data.default_charts;
          $scope.buyers = response.data.data.buyers;
          $scope.departments = response.data.data.departments;
          $scope.members = response.data.data.members;
        });
      }

      function setSelectedMember(member) {
        $scope.selectedMember = member;
        params.member = member;

        dashboardService.getFilteredData(params).then(function(response) {
          console.log("Response: ", response);
          $scope.charts = response.data.data.default_charts;
          $scope.buyers = response.data.data.buyers;
          $scope.departments = response.data.data.departments;
          $scope.members = response.data.data.members;
        });
      }
}])
    .factory('dashboardService', ['$http', function ($http) {

      return {
        getFilteredData: getFilteredData
      };

      function getFilteredData(params) {
        return $http.get('/dashboard/data/', {params: params});
      }
    }]);
