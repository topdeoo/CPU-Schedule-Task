import gurobipy as gp
from gurobipy import GRB


def callback(model, where):
    if where == GRB.Callback.MIPSOL:
        # Get the violated constraint
        violated_constr = model.cbGetConstrs()[0]  # Get the first violated constraint
        print("Violated constraint:", violated_constr.ConstrName)


def solve_cpu_scheduling(
    M, Ts, Te, N, Cores, MCores, EarliestStart, LatestStart, Duration
):
    model = gp.Model("CPU Scheduling")

    # Create variables
    X = model.addVars(N, M, vtype=GRB.BINARY, name="X")
    Start = model.addVars(N, M, vtype=GRB.INTEGER, lb=0, name="Start")
    R = model.addVars(max(Te) + 1, N, M, vtype=GRB.BINARY, name="R")

    # Set objective
    model.setObjective(
        gp.quicksum(
            X[i, k] * Duration[i] * Cores[i] for i in range(N) for k in range(M)
        ),
        GRB.MAXIMIZE,
    )

    # constraints
    model.addConstrs((X.sum(i, "*") <= 1 for i in range(N)), name="one_job_per_machine")
    model.addConstrs(
        (
            (Start[i, k] + Duration[i]) * X[i, k] <= Te[k]
            for k in range(M)
            for i in range(N)
        ),
        name="end_time",
    )
    model.addConstrs(
        (
            Start[i, k] * X[i, k] >= X[i, k] * max(Ts[k], EarliestStart[i])
            for k in range(M)
            for i in range(N)
        ),
        name="start_time",
    )
    model.addConstrs(
        (Start[i, k] * X[i, k] <= LatestStart[i] for k in range(M) for i in range(N)),
        name="latest_start_time",
    )

    # FIXME: core constraint not correct
    """
    problem in constraints core_1 core_2
    as the core_1 and core_2 may be conflict with each other

    core_3 make sure that only one job can be assigned to one core at a time
    """

    model.addConstrs(
        (
            R[t, i, k] >= (Start[i, k] * X[i, k] - t + 1)
            for k in range(M)
            for i in range(N)
            for t in range(EarliestStart[i], min(LatestStart[i] + Duration[i], Te[k]))
        ),
        name="core_1",
    )
    model.addConstrs(
        (
            R[t, i, k] <= (Start[i, k] * X[i, k] - t - 1 + Duration[i])
            for k in range(M)
            for i in range(N)
            for t in range(EarliestStart[i], min(LatestStart[i] + Duration[i], Te[k]))
        ),
        name="core_2",
    )
    model.addConstrs(
        (
            R.sum(t, i, "*") <= 1
            for i in range(N)
            for k in range(M)
            for t in range(EarliestStart[i], min(LatestStart[i] + Duration[i], Te[k]))
        ),
        name="core_3",
    )

    for k in range(M):
        expr = gp.QuadExpr()
        for i in range(N):
            for t in range(EarliestStart[i], min(LatestStart[i] + Duration[i], Te[k])):
                expr.addTerms(Cores[i], R[t, i, k], X[i, k])
        model.addConstr(expr <= MCores[k])

    # Solve the model
    model.optimize()

    if model.status == GRB.OPTIMAL:
        # Print solution
        print("Optimal solution found!")
        for i in range(N):
            for k in range(M):
                print(f"Job {i} is assigned to machine {k}.")
                print(f"Start time: {Start[i, k].x}")
                if X[i, k].x > 0.5:
                    print(f"solution: Job {i} is assigned to machine {k}.")
                    print(f"solution: Start time: {Start[i, k].x - 1}")
        for r in R:
            print(f"R[{r}] = {R[r].x}")
        print(f"Optimal objective value: {model.objVal}")
    else:
        model.computeIIS()
        model.write("model.ilp")
        print("No feasible solution found.")


# Example usage
M = 2
Ts = [1, 1]
Te = [25, 25]
MCores = [65535, 65535]
N = 4
Cores = [2, 3, 1, 2]
EarliestStart = [1, 4, 1, 5]
LatestStart = [4, 5, 2, 6]
Duration = [2, 2, 4, 3]

solve_cpu_scheduling(M, Ts, Te, N, Cores, MCores, EarliestStart, LatestStart, Duration)
