import Plot from 'react-plotly.js';

function TestPlot2() {

  // Function to generate data points for a normal distribution
  const generateNormalDistribution = (mean, stdDev, size) => {
    const data = [];
    for (let i = 0; i < size; i++) {
      const x = i;
      const y = (1 / (stdDev * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * ((x - mean) / stdDev) ** 2);
      data.push({ x, y });
    }
    return data;
  };

  const mean = 10;
  const stdDev = 3; 
  const size = 100; 

  const normalDistributionData = generateNormalDistribution(mean, stdDev, size);

  return (
    <div className="Plot">
      <Plot
        data={[
          {
            x: normalDistributionData.map(point => point.x),
            y: normalDistributionData.map(point => point.y),
            mode: 'lines',
            type: 'scatter',
          },
        ]}
        layout={{
          title: 'Title',
          xaxis: {
            title: 'X-axis',
          },
          yaxis: {
            title: 'Y-axis',
          },
          autosize: true,
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}

export default TestPlot2;