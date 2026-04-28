# 07 Fail-Closed — The Structure Stops



<!-- FILE: 07_fail_closed_EN.md -->



---



## Why “saying I don't know” is not enough



For many years people have said the following about AI honesty.



> “An AI should be able to say ‘I don't know’.”



This observation is correct.



But it is **not sufficient as a solution**.



Whether an AI says “I don't know” depends on intention or training.

It depends on whether the system chooses to be honest at that moment.



That is a behavioral question.



It is not a structural guarantee.



NRA-IDE approaches this differently.



---



## The structure stops



The moment



```

R ≥ 1.0

```



the output stops.



No decision-maker is required.

No intention to be honest is required.



The fact that the structural limit has been exceeded becomes the reason for stopping.



There is simply **no structural path that allows the system to continue**.



The log records only the structural state.



For example:



```

R = 1.032

τ = 0.14

δ = 0.15

output stopped

```



The system does not say “I did not know”.



Instead, it records **the structural condition** that caused the stop.



The system does not choose to stop.



**The structure stops it.**



---



## The danger of systems that cannot stop



Most current AI systems are trained to always produce an answer.



Even when information is insufficient, they generate something.



This is a design choice.



But it creates a structural problem.



The system continues operating **even after the structural limit has been exceeded**.



Imagine a dam that has already collapsed, while pumps continue forcing water into it.



As long as the structure is broken, every attempt makes the damage worse.



Repeated regeneration of answers is similar.



The system simply stacks new outputs on top of a broken structure.



Fail-Closed cuts this chain **structurally**.



---



## Stopping is not the end



As described in Chapter 05,



```

SILENCE  : R ≥ 1.0 and ω > 0

```



is a transition.



The system has exceeded the range it can safely handle.



The task is therefore passed to the next responsible agent — usually a human.



Water does not stop flowing.



The direction simply changes.



---



Two states must be distinguished.



**SILENCE**



The structure continues moving.

Responsibility is handed over to the next agent.



**HALT**



The structure has lost motion.

No transition is possible.



HALT is the most dangerous state.



Fail-Closed is designed to ensure that the system enters **SILENCE**, not HALT.



---



## Safety is not judged each time



Traditional safety mechanisms attempt to judge each output.



Filters.

Guardrails.

Moderation systems.



All of them evaluate **meaning** after the output is produced.



NRA-IDE is different.



Instead of judging safety each time, it creates a structure that **cannot continue once the limit is exceeded**.



The system does not need to decide whether the output is safe.



It only evaluates the structural state.



---



## What Fail-Closed guarantees



Fail-Closed does **not guarantee correct answers**.



It guarantees only one thing.



The system **does not produce output after the structural limit has been exceeded**.



This may seem like a small guarantee.



But it is something that “always-answer” systems cannot guarantee at all.



The behavior after exceeding the limit is already determined at the design stage.



---



In the next chapter we examine how these structural limit events are recorded.

