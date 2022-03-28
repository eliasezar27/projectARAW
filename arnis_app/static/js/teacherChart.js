$(document).ready(function() {

    req = $.ajax({
            url : '/section/count/perTrack',
            type : 'GET'
        });

    req.done(function(data) {

        console.log(data.result);

        const ctx = document.getElementById('stackCol').getContext('2d');

        const labels = data.labels;
        const dataQuery = {
          labels: labels,
          datasets: [
            {
                data: data.sectionCounts,
                backgroundColor: '#ba022a'
            },
          ]
        };

        const config = {
          type: 'bar',
          data: dataQuery,
          options: {
            plugins: {
              title: {
                display: true,
                text: 'Assigned Sections per Track'
              },
              legend: {
                display: false,
              },
            },
            responsive: true,
            scales: {
                    x:{
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    },
                    y:{
                        grid: {
                            display: false,
                            drawBorder: false
                        }
                    },
                },
          },
        };

        const stackCol = new Chart(ctx, config)
    });
});
