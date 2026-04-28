# 11 Domain Tuning — Adapting NRA-IDE to Different Fields



<!-- FILE: 11_domain_tuning_EN.md -->



---



## Why domain tuning is necessary



NRA-IDE provides a structural evaluation framework.



However, the framework itself does not define the concrete variables used in each system.



Every real system operates within a specific physical or operational environment.



For this reason, NRA-IDE must be adapted to the **domain in which it is applied**.



This process is called **Domain Tuning**.



---



## Structural parameters are domain dependent



The core structural relationship of NRA-IDE is



```id="g4kqz5"

R = δ / τ

```



where



```

δ : deviation from the structural constraint  

τ : thickness of the constraint boundary

```



The mathematical relationship remains the same across domains.



However, the **observables used to measure δ and τ differ depending on the system**.



Therefore, each domain must determine which quantities represent structural deviation and constraint thickness.



---



## Examples of domain-specific observables



Different fields require different observables.



For example:



Autonomous driving systems may evaluate variables such as



```id="qjhz4f"

distance to obstacle

relative velocity

lane confidence

yaw rate deviation

time margin before stop

```



Medical monitoring systems may evaluate



```id="b9c9pb"

vital sign deviation

physiological stability ranges

drug infusion limits

```



Infrastructure monitoring systems may evaluate



```id="m5x7yu"

structural stress

vibration patterns

water pressure

load fluctuations

```



In every case, the specific measurements differ, but the structural evaluation remains the same.



---



## Domain knowledge is essential



Correct domain tuning requires **expert knowledge of the system being monitored**.



The framework itself cannot determine which observables are meaningful.



Engineers and operators who understand the physical system must define the appropriate parameters.



Without this step, structural evaluation may become incomplete or misleading.



---



## Avoiding parameter transplantation



One common mistake is to reuse parameters from one domain in another.



This approach may appear convenient, but it often leads to incorrect evaluations.



Each domain has its own structural constraints, physical limits, and operational conditions.



Domain tuning must therefore be performed **independently for each system**.



---



## NRA-IDE as a structural template



NRA-IDE should be understood as a **structural template** rather than a fixed algorithm.



The framework defines



* how structural limits are evaluated

* how thresholds are handled

* how systems transition to Fail-Closed behavior



But the concrete implementation depends on the domain.



This flexibility allows the same framework to be used in many different fields.



---



## The boundary remains the same



Although the observables differ across domains, the fundamental boundary rule remains unchanged.



When



```id="ksl3bc"

R ≥ 1.0

```



the structural limit has been exceeded.



At this point the system must transition to **SILENCE** or **Fail-Closed behavior**.



This rule is universal within the NRA-IDE framework.



---



## A framework for many systems



Because the framework separates structural evaluation from domain-specific measurement, it can be applied across a wide range of systems.



Possible application areas include



* autonomous systems

* medical monitoring

* infrastructure safety

* industrial process control

* environmental monitoring



In each case, the framework provides a consistent method for determining whether a system remains within its safe structural boundary.



---



The next chapter provides a glossary of the key terms used throughout the NRA-IDE documentation.

