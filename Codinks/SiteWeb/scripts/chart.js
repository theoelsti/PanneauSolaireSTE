// Bon ba le graphique tavu
Chart.defaults.global.defaultFontFamily ='Lato';
var ctx = document.querySelector('#meteoChart').getContext('2d');  
/*
  o__ __o                   o                  
 <|     v\                 <|>                 
 / \     <\                < >                 
 \o/       \o    o__ __o/   |         o__ __o/ 
  |         |>  /v     |    o__/_    /v     |  
 / \       //  />     / \   |       />     / \ 
 \o/      /    \      \o/   |       \      \o/ 
  |      o      o      |    o        o      |  
 / \  __/>      <\__  / \   <\__     <\__  / \ 
*/
var data = {
    labels: timeStamps,
    datasets: [
    {
        label:'Raffales (en km/h)',
        color:'#FFFFFF',
        backgroundColor: '#40d0d310',
        borderColor: '#40d0d3',
        data: raffales
    },
    {
        label:'Vent Moyen (en km/h)',
        color:'#80d0d0',
        backgroundColor: '#80d0d010',
        borderColor: '#80d0d0',
        data: medians
    },
    {
        label:'Seuil (en km/h)',
        color:'#d21d19',
        backgroundColor: '#d21d1955',
        borderColor: '#d21d19',
        data: seuil
    }
  
  ]}

/*
      o__ __o                   o        o                                      
     /v     v\                 <|>     _<|>_                                    
    />       <\                < >                                              
  o/           \o   \o_ __o     |        o      o__ __o    \o__ __o       __o__ 
 <|             |>   |    v\    o__/_   <|>    /v     v\    |     |>     />  \  
  \\           //   / \    <\   |       / \   />       <\  / \   / \     \o     
    \         /     \o/     /   |       \o/   \         /  \o/   \o/      v\    
     o       o       |     o    o        |     o       o    |     |        <\   
     <\__ __/>      / \ __/>    <\__    / \    <\__ __/>   / \   / \  _\o__</   
                    \o/                                                         
                     |                                                          
                    / \                                                         
*/
var options = { 
    title:{
        display:true,
        text:'Valeurs des prochaines 24h ',
        fontSize:40,
        fontColor:'#FFFFFF',
        fontFamily:'arial'
    },
    legend:{
        position:'bottom'
    },
    scales:{
        yAxes: [{
        id: 'A',
        type: 'linear',
        position: 'left',
        ticks: {
          max: 170,
          min: 0,
          fontColor:'#FFFFFF',
          fontSize: 15
        }
      }, {
        id: 'B',
        type: 'linear',
        position: 'right',
        ticks: {
          max: 170,
          min: 0,
          fontColor:'#FFFFFF',
          fontSize: 15
        }
      }],
      xAxes:[{
        ticks: {
          fontColor:'	#FFFFFF',
          fontSize: 13
        }
      }]
    }
}

/*
      o__ __o                              o__ __o      o                          
     /v     v\                            /v     v\   _<|>_                        
    />       <\                          />       <\                               
  o/               o__ __o    \o__ __o   \o             o      o__ __o/      __o__ 
 <|               /v     v\    |     |>   |>_          <|>    /v     |      />  \  
  \\             />       <\  / \   / \   |            / \   />     / \     \o     
    \         /  \         /  \o/   \o/  <o>           \o/   \      \o/      v\    
     o       o    o       o    |     |    |             |     o      |        <\   
     <\__ __/>    <\__ __/>   / \   / \  / \           / \    <\__  < >  _\o__</   
                                                                     |             
                                                             o__     o             
                                                             <\__ __/>             
*/
var config = {
  type: 'line',
  data: data,
  options: options
  }

  Chart.plugins.register({
    beforeDraw: function(chartInstance, easing) {
      var ctx = chartInstance.chart.ctx;
      ctx.fillStyle = '		#30122d'; // your color here
  
      var chartArea = chartInstance.chartArea;
      ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
    }
  });
let chartmeteo = new Chart(ctx, config);

/*
         o            o__ __o      o__ __o      o                o                                               
        <|>          /v     v\    /v     v\   _<|>_             <|>                                              
        / \         />       <\  />       <\                    / >                                              
      o/   \o       \o           \o             o        __o__  \o__ __o       o__ __o/    o__ __o/    o__  __o  
     <|__ __|>       |>_          |>_          <|>      />  \    |     v\     /v     |    /v     |    /v      |> 
     /       \       |            |            / \    o/        / \     <\   />     / \  />     / \  />      //  
   o/         \o    <o>          <o>           \o/   <|         \o/     o/   \      \o/  \      \o/  \o    o/    
  /v           v\    |            |             |     \\         |     <|     o      |    o      |    v\  /v __o 
 />             <\  / \          / \           / \     _\o__</  / \    / \    <\__  / \   <\__  < >    <\/> __/> 
                                                                                                 |               
                                                                                         o__     o               
                                                                                         <\__ __/>               
*/
// $("#10").on("click", function() {
//   chartmeteo.destroy()
//   var context1 = document.getElementById('meteoChart').getContext('2d');
//   showHoursButtons()
//   showMinutesButtons()
//   show = 0;
//   switchShow()
//   context1.style.backgroundColor = 'rgba(255,0,0,255)';
//   chartmeteo = new Chart(context1, config);});

/*
  o__ __o__/_                                 o        o                                      
 <|    v                                     <|>     _<|>_                                    
 < >                                         < >                                              
  |         o__ __o    \o__ __o       __o__   |        o      o__ __o    \o__ __o       __o__ 
  o__/_    /v     v\    |     |>     />  \    o__/_   <|>    /v     v\    |     |>     />  \  
  |       />       <\  / \   / \   o/         |       / \   />       <\  / \   / \     \o     
 <o>      \         /  \o/   \o/  <|          |       \o/   \         /  \o/   \o/      v\    
  |        o       o    |     |    \\         o        |     o       o    |     |        <\   
 / \       <\__ __/>   / \   / \    _\o__</   <\__    / \    <\__ __/>   / \   / \  _\o__</   
                                                                                              
*/


// 0xFadeath Copyrigthed this