$(document).ready(function() {

    req = $.ajax({
            url : '/section/count/perTrack',
            type : 'GET'
        });
let delayed;
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
                        },
                        title: {
                            display: true,
                            text: "# of Sections"
                        }

                    },

                },
                animation: {
                  onComplete: () => {
                    delayed = true;
                  },
                  delay: (context) => {
                    let delay = 0;
                    if (context.type === 'data' && context.mode === 'default' && !delayed) {
                      delay = context.dataIndex * 300 + context.datasetIndex * 1000;
                    }
                    return delay;
                  },
            },
          },
        };

        const stackCol = new Chart(ctx, config)
    });
});
