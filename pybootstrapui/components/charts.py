from .base import HTMLElement
from typing_extensions import deprecated


@deprecated('Bad Code')
class AnalyticsChart(HTMLElement):
	"""
	A class to generate an analytics chart (line chart) using Chart.js.

	Warning:
		# Deprecated:
		- This class may not work correctly due to outdated or incomplete implementation.
		- Use this only as a basic example or for debugging purposes.

	Attributes:
		- `labels` (list[str]): The labels for the chart (e.g., categories on the X-axis).
		- `values` (list[float]): The values for the chart (e.g., data points on the Y-axis).
		- `chart_label` (str): The label for the chart dataset.
		- `bg_color` (tuple[int, int, int, float]): The background color for the chart (RGBA).
		- `border_color` (tuple[int, int, int, float]): The border color for the chart (RGBA).
		- `thickness` (int): The thickness of the chart border line.
	"""

	def __init__(self, chart_labels: list[str], chart_values: list[float], unique_id: str, chart_label: str,
				 classes: list[str] | None = None,
				 bg_color: tuple[int, int, int, float] = (24, 247, 12, 0.8),
				 border_color: tuple[int, int, int, float] = (24, 247, 12, 1),
				 thickness: int = 3):
		"""
		Initializes the AnalyticsChart with provided labels, values, and optional properties.

		Warning:
			- This class is deprecated and may not function as expected in modern Chart.js versions.

		Parameters:
			- `chart_labels` (list[str]): The chart labels.
			- `chart_values` (list[float]): The data points corresponding to the labels.
			- `unique_id` (str): The unique ID for the canvas element.
			- `chart_label` (str): The label for the dataset.
			- `classes` (list[str] | None): Optional list of classes for styling the chart.
			- `bg_color` (tuple[int, int, int, float]): Optional background color (RGBA).
			- `border_color` (tuple[int, int, int, float]): Optional border color (RGBA).
			- `thickness` (int): The thickness of the border line for the chart.

		Raises:
			- `ValueError`: If the lengths of `chart_labels` and `chart_values` do not match.
		"""
		super().__init__(classes, unique_id)
		if len(chart_values) != len(chart_labels):
			raise ValueError('Length of chart_labels must be equal to chart_values!')

		self.labels = chart_labels
		self.values = chart_values
		self.chart_label = chart_label
		self.bg_color = f'rgba({",".join(map(str, bg_color))})'
		self.border_color = f'rgba({",".join(map(str, border_color))})'
		self.thickness = thickness

	def construct(self):
		"""
		Generates the HTML code for embedding the chart in a webpage.

		Returns:
			- `str`: The HTML and JavaScript code to render the chart.

		Warning:
			- This method generates inline JavaScript, which may not be ideal for production environments.
		"""
		return f'''
		<canvas class="histogram {self.classes_str}" id="{self.id}"></canvas>
		<script>
			console.warn("AnalyticsChart is deprecated and may not render correctly.");
			var ctx = document.getElementById('{self.id}').getContext('2d');
			new Chart(ctx, {{
				type: 'line',
				data: {{
					labels: {self.labels},
					datasets: [{{
						label: "{self.chart_label}",
						data: {self.values},
						fill: true,
						cubicInterpolationMode: 'monotone',
						backgroundColor: '{self.bg_color}',
						borderColor: '{self.border_color}',
						borderWidth: {self.thickness},
						borderJoinStyle: 'bevel'
					}}]
				}},
				options: {{
					responsive: true,
					scales: {{
						y: {{
							beginAtZero: true,
							ticks: {{
								color: 'rgba(255, 255, 255, 0.6)'
							}}
						}},
						x: {{
							ticks: {{
								color: 'rgba(255, 255, 255, 0.6)'
							}}
						}}
					}},
					plugins: {{
						legend: {{
							display: false,
							labels: {{
								color: 'rgba(255, 255, 255, 0.8)'
							}}
						}},
						tooltip: {{
							titleColor: 'rgba(255, 255, 255, 0.8)',
							bodyColor: 'rgba(255, 255, 255, 0.8)'
						}}
					}}
				}}
			}});
		</script>
		'''
