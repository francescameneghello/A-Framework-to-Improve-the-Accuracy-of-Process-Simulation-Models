# A-Framework-to-Improve-the-Accuracy-of-Process-Simulation-Models

Business process simulation is a methodology that enables analysts to run the process in different scenarios, compare the performances and con-
sequently provide indications into how to improve a business process. Process simulation requires one to provide a simulation model, which should accurately
reflect the reality to ensure the reliability of the simulation findings. This paper proposes a framework to assess the extent with which a simulation model reflects
reality and to pinpoint how to reduce the distance. The starting point is a business simulation model, along with a real event log that records actual executions of the
business process being simulated and analyzed. In a nutshell, the idea is to simulate the process, thus obtaining a simulation log, which is subsequently compared
with the real event log. A decision tree is built, using the vector of features that represent the behavioral characteristics of log traces. The tree aims to classify
traces as belonging to the real and simulated event logs, and the discriminating features encode the difference between reality, represented in the real event log, and the simulation model, represented in the simulated event logs. These features provide actionable insights into how to repair simulation models to become closer to reality. The technique has been assessed on a real-life process for which the literature provides a real event log and a simulation model. The assessment results show that the initial, given simulation model was not sufficiently accurate, but that our framework enables repairing it to better reflect the reality.
