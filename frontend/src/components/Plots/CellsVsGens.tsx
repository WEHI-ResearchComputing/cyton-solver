import * as React from "react";
import Plot from 'react-plotly.js';
import { ExtrapolationResults } from "../../client"

export function CellsVsGens({ extrapolationData, timepoint }: { extrapolationData: ExtrapolationResults, timepoint: number }) {
  return (
    <div className="Plot">
      <Plot
        data = {[
          {
            y: extrapolationData.hts.cells_gen.map(genData => genData[timepoint]),
            mode: "lines+markers",
            type: "scatter"
          }
        ]}
        layout={{
          title: `Live Cells vs Generations at HT ${timepoint + 1}`,
          xaxis: {
            title: "Generation Number",
          },
          yaxis: {
            title: "Number of Cells",
          },
          autosize: true,
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
