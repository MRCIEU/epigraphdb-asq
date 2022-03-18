import _ from "lodash";

export function makeHistogramOptions(
  series: Array<number>,
  title: string,
): Record<string, any> {
  const binsNumber = series.length > 10 ? series.length / 2 : series.length;
  const res = {
    title: {
      text: title,
    },
    subtitle: {
      text: "Scatter plot and histogram",
    },
    xAxis: [
      {
        title: { text: "Observations" },
        visible: false,
        // alignTicks: false,
      },
      {
        title: { text: "Histogram" },
        alignTicks: false,
        plotLines: [
          {
            color: "#E65100",
            width: 5,
            value: 1,
          },
        ],
        // opposite: true,
      },
    ],
    yAxis: [
      {
        title: { text: "Observations" },
        visible: false,
      },
      {
        title: { text: "Histogram" },
        // opposite: true,
      },
    ],
    series: [
      {
        name: "Histogram count",
        type: "histogram",
        binsNumber: binsNumber,
        xAxis: 1,
        yAxis: 1,
        baseSeries: "s1",
        zIndex: -1,
        color: "#00796B",
      },
      {
        name: "Observation",
        type: "scatter",
        data: series,
        color: "#F9A825",
        id: "s1",
        marker: {
          radius: 3,
        },
      },
    ],
    credits: {
      enabled: false,
    },
  };
  return res;
}
