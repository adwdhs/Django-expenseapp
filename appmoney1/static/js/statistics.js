

const chartRender=(data, labels)=>{


const datasets = [{
    label: 'Last 6 months expenses',
    data: data,
    backgroundColor: [
      'rgba(255, 99, 132, 0.2)',
      'rgba(255, 159, 64, 0.2)',
      'rgba(255, 205, 86, 0.2)',
      'rgba(75, 192, 192, 0.2)',
      'rgba(54, 162, 235, 0.2)',
      'rgba(153, 102, 255, 0.2)',
      'rgba(96, 96, 96, 0.2)',
      'rgba(0, 0, 204, 0.2)',
      'rgba(0, 153, 0, 0.2)',
    ],
    borderColor: [
      'rgb(255, 99, 132)',
      'rgb(255, 159, 64)',
      'rgb(255, 205, 86)',
      'rgb(75, 192, 192)',
      'rgb(54, 162, 235)',
      'rgb(153, 102, 255)',
      'rgb(96, 96, 96)',
      'rgb(0, 0, 204)',
      'rgb(0, 153, 0)',
    ],
    borderWidth: 1
  }];

new Chart("firstchart", {
  type: "doughnut",
  data: {
    labels: labels,
    datasets: datasets
  },
  options: {
  title:{
  display:true, text:'Expenses per Category'}}
});
new Chart("secondchart", {
  type: "bar",
  data: {
    labels: labels,
    datasets: datasets
  },
  options: {
  title:{
  display:true, text:'Expenses per Category'}}
});
}

const getChartData=()=>{
    console.log('fetching')
    fetch('http://127.0.0.1:8000/summary')
    .then(response => response.json())
    .then(results => {
        console.log('results', results);
        const category_data=results.expenses_sum_data
        const [labels, data] = [
            Object.keys(category_data),
            Object.values(category_data),
        ];

        chartRender(data, labels);
    });


};


document.onload=getChartData();



