angular.module("app", ["highcharts-ng", "daterangepicker", "app.config"])
    .config(['$interpolateProvider', '$compileProvider', function($interpolateProvider, $compileProvider) {
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');

        $compileProvider.debugInfoEnabled(false);
    }])
    .controller('DashboardCtrl', ['$scope', 'dashboardService', 'SERVER_CONFIG', function ($scope, dashboardService, SERVER_CONFIG) {

      $scope.dimensions = [
          'Company',
          'Requester Name',
          'Department',
          'Category',
          'Description',
          'Delivery Location',
          'Emergency',
          'Status',
          'Buyer'
      ];
      $scope.measures = [
          'Request Number',
          'Request Date',
          'Total Estimated Price',
          'Date Required',
          'Sample Required',
          'Total Quote Price',
          'Savings amount',
          'Savings %'
      ];
      $scope.aggregateFunctions = [
          'size',
          'sum',
          'mean'
      ];
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
      $scope.customCharts = [];
      $scope.addingChart = false;
      $scope.createChart = createChart;
      $scope.toggleForm = toggleForm;

      $scope.selectedBuyer = 'Buyer';
      $scope.setSelectedBuyer = setSelectedBuyer;
      $scope.selectedDepartment = 'Department';
      $scope.setSelectedDepartment = setSelectedDepartment;
      $scope.selectedMember = 'Team member';
      $scope.setSelectedMember = setSelectedMember;
      var params = {};

      ///
      function setSelectedBuyer(buyer) {
        if(buyer === undefined) {
          $scope.selectedBuyer = 'Buyer';
          params.buyer = '';
        } else {
          $scope.selectedBuyer = buyer;
          params.buyer = buyer;
        }

        dashboardService.getFilteredData(params).then(function(response) {
          console.log("Response: ", response);
          $scope.charts = response.data.data.default_charts;
          $scope.buyers = response.data.data.buyers;
          $scope.departments = response.data.data.departments;
          $scope.members = response.data.data.members;
        });
      }

      function setSelectedDepartment(department) {
        if(department === undefined) {
          $scope.selectedDepartment = 'Department';
          params.department = '';
        } else {
          $scope.selectedDepartment = department;
          params.department = department;
        }

        dashboardService.getFilteredData(params).then(function(response) {
          console.log("Response: ", response);
          $scope.charts = response.data.data.default_charts;
          $scope.buyers = response.data.data.buyers;
          $scope.departments = response.data.data.departments;
          $scope.members = response.data.data.members;
        });
      }

      function setSelectedMember(member) {
        if(member === undefined) {
          $scope.selectedMember = 'Member';
          params.member = '';
        } else {
          $scope.selectedMember = member;
          params.member = member;
        }

        dashboardService.getFilteredData(params).then(function(response) {
          console.log("Response: ", response);
          $scope.charts = response.data.data.default_charts;
          $scope.buyers = response.data.data.buyers;
          $scope.departments = response.data.data.departments;
          $scope.members = response.data.data.members;
        });
      }

      function toggleForm() {
        $scope.addingChart = !$scope.addingChart;
      }

      function createChart() {
        var chartParams = {
          dimension: $scope.selectedDimension,
          measure: $scope.selectedMeasure,
          aggregateFunction: $scope.selectedAggregateFunction
        };

        dashboardService.generateChart(chartParams).then(function(response) {
          console.log("Generate chart response: ", response);
          $scope.customCharts.push(response.data.data);
          $scope.addingChart = !$scope.addingChart;
        });
      }
}])
    .factory('dashboardService', ['$http', function ($http) {

      return {
        getFilteredData: getFilteredData,
        generateChart: generateChart
      };

      function getFilteredData(params) {
        return $http.get('/dashboard/data/', {params: params});
      }

      function generateChart(params) {
        return $http.get('/dashboard/create-chart/', {params: params})
      }
    }]);
