import Plot from 'react-plotly.js';

function TestPlot() {

  
  return (
    <div
      className="Plot"
      style={{
        // display: "flex",
        // justifyContent: "center",
        // alignItems: "center",
        // height: "100vh",

      }}
    >
      <Plot
        data={[
          {
            x: [1, 2, 3, 4, 6, 8, 10, 12, 14, 16, 18],
            y: [32, 37, 40.5, 43, 49, 54, 59, 63.5, 69.5, 73, 74],
            mode: "markers+lines",
            type: "scatter",
          },
        ]}
        layout={{
          title: "Title",
          xaxis: {
            title: "X-axis",
          },
          yaxis: {
            title: "Y-axis",
          },
          autosize: true,  // Allow the chart to be responsive
        }}
        style={{ width: '100%', height: '100%'}} 
      />
    </div>
  );
}

export default TestPlot;