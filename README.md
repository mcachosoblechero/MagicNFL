# Pocket Penetration Score for Offensive Linemen

# Introduction

Lineman is one of the most crucial roles on the offensive team, providing the QB with the much needed time and space to find the ideal pass. Despite its offensive importance, there is no clear metric to define its performance as a unit, complicating the comparison across teams while making the offensive line a great unknown for fans.

# Why is this important?

The NFL is transforming the game through data, improving its analytics to drive fan engagement while bringing the players closer to the general public. This has been done successfully with several positions:
- QBs are evaluated by the number of passes completed, the number of yards achieved, and the number of touchdowns and interceptions thrown.
- WRs can be compared based on the yards achieved after catch and touchdowns.

This has enabled coaches to understand a player's impact in the game, tracking and comparing individual performance throughout the season. For fans, this has been an opportunity to get closer to their heroes while getting further insights on the game.

However, when it comes to the offensive line, no clear metric has been developed to measure and compare unit performance. Its main role in passing plays is to protect the QB, but performance is usually tightly coupled with the rest of the offensive team.

Consider, for example, an instance where the Quarterback scrambles out of the pocket but throws a touchdown pass. This is unambiguously good for the offense but it is ambiguous whether the offensive line performed well.

This proposal addresses this gap, analyzing and isolating the role of offensive linemen. We propose a mathematical framework to evaluate unit performance by creating a single metric, the “Pocket Penetration Score” (PPS). By quantifying performance, the PPS has the potential to serve both coaches and fans, providing the much needed ground for comparison between offensive line units. 

# The Question

**How well did the offensive linemen protect the field area that the QB uses to throw the football?** 

This question puts the focus on the pocket area used by the QB. This enables us to isolate the offensive line's impact on the play, as protecting this area is solely the responsibility of the players who are given blocking assignments, unlike the other aggregate metrics.  

Furthermore, this question aims to encapsulate the unit-level performance which, unlike individual player analysis, provides a more holistic perspective on how the performance of the offensive line impacts the overall team performance.

*We recognize that this question can also be used to address the corollary: How well did the defensive line attack the pocket. However, for consistency, we will frame our analysis from the perspective of the offensive line.*

# Our Approach: The Pocket Penetration Score
To answer this question, we define the QB pocket as a circular area that the offensive line protects from defensive rushers. We measure the linemen's performance on this task using our "Pocket Penetration Score" (PPS), which represents the pressure the defensive line exerts into the pocket. This score can increase in two ways:
- Pass rushers penetrating the pocket area increases the score as they approach the center of the pocket
- QB leaving the pocket sharply increases the score as the QB flees the pass rush

Thus, the goal of the offensive linemen is to keep this score as low as possible by preventing the defense from entering the pocket while keeping the QB in-pocket. 

This framing raises the following questions:
- What pocket area needs protection by the offensive line?
- How valuable is the pocket area?
- How much pressure do the defensive players exert on the pocket?
- How do we judge the offensive line if the quarterback is forced to flee?
- Which single metric captures the above questions succinctly and efficiently?

## 1. What pocket area needs protection by the offensive line?

**For this analysis, we define the pocket to be the circle centered 7.5 yards behind the line of scrimmage with a radius of 7.5 yards.** 

From visual analysis, this is a consistent way of determining the pocket across different plays and formations.  The choice of a circle was chosen because that is the approximate shape that the offensive line ends up forming as the offensive tackles attempt to push their rushers "out-and-up". 

![download](https://user-images.githubusercontent.com/10617948/211914959-2327cb6c-3b20-4c31-80ef-f593b9907b39.gif)

## 2. How valuable is the pocket area?

**The value of the pocket area is determined by a Gaussian distribution centered at 7.5 yards behind the scrimmage line, with a mean of 0 and a sigma of 1.**

This Field Price (FP) is represented mathematically as:

$$FP \sim Normal \; (\mu,\sigma^2)$$

This made theoretical sense because a defensive player should cause a QB to panic only when they are getting very close. 

## 3. How much pressure do the defensive players exert on the pocket?

**A defensive player exerts pressure following by a Gaussian distribution around them, with a mean of 0 and a sigma of 1**

The Player Influence (PI) is mathematically represented as:

$$PI \sim Normal \; (0,1) \text{ centered at }(x_{player}, y_{player})$$

The sigma here was chosen because this is the approximate arm-length for defensive players.

Based on these two questions, the In-Pocket Price (IPP) paid by the Offensive Linemen at a specific frame follows this equation:

$$IPP_i = \sum_{n=1}^{\text{def players}} PI_n(x_n, y_n) * FP$$

## 4. How do we judge the offensive line if the quarterback is forced to flee?

**We treat a QB being forced to flee as a failure of the offensive line, and penalize them according to an inverted Gaussian with a mean of 0, sigma of 1 with a maximum value of 800, centered at the edge of the pocket. This penalty is applied once the QB crosses the 7.5 yards pocket boundary**

We wanted to ensure that the offensive line was penalized when the Quarterback was forced to flee the pocket because it meant that the defensive line was exerting their influence on the play. However, we also wanted to recognize the fact that a Quarterback is expected to move around inside the pocket. Thus, the offensive line is penalized only when the Quarterback leaves the pocket.

This Out-Of-Pocket Price (OOPP) at a specific frame is mathematically represented as follows:

$$OOPP_i(x_{QB_i}, y_{QB_i})= 
\begin{cases}
    Pen_{OOP}(1-Normal \; (0,1) \text{ centered at }(R-7.5)),& \text{if } R\geq 7.5\\
    0,              & \text{otherwise}
\end{cases}$$

where $Pen_{OOP} = 800$ and $R=\sqrt((x_{qb} - x_{pocket center})^2 - (y_{qb} - y_{pocket center})^2)$

## 5. Which single metric captures the above questions succinctly and efficiently?

The final Pocket Penetration Score (PPS) is a combination of the In-Pocket Price and the Out-of-Pocket Price.
For each frame i, we obtain the associated PPS as follows:

$$PPS_i = \text{IPP}_i + \text{OOPP}_i$$

The single PPS score is considered the maximum value across frames in a single play

$$PPS = max(PPS_i)$$

# Pocket Penetration Score in Action

To evaluate the predictive capabilities of our Pocker Penetration Score (or PPS), we will explore its impact from 3 perspectives:
- Individual Plays, looking it evolution during plays with different outcome
- Game Analysis, exploring its correlation with high-level metrics
- Season Performance, understanding the relationship between team performance and PPS

These analyses will include "traditional" pass plays only. While we think this metric could be meaningfully applied to boots and other non-dropback passes, for our initial presentation we include only plays where the offense lines up in a dropback/shotgun formation and plays where the QB was forced to scramble.

## 1. Individual Plays
Let's start looking at the Pocket Penetration Score play-by-play. For each individual play, we have considered three possible scenarios with distinct score profiles:
- **QB remains in-pocket and passes the football**
- **QB remains in-pocket and gets sacked**
- **QB runs out of pocket**

We calculated the evolution of the Pocket Penetration Score across time, categorizing the plays based on these three scenarios. The result can be found in the figure below. The shaded regions represent 95% confidence intervals. 

We see that when the QB remained in the pocket and successfully threw a pass (Blue), the PPS has a slower increase and a lower maximum value.  Conversely, when the QB is sacked inside the pocket (Green), we see a steep increase in PPS coupled with a higher maximum value.  The third option, where the QB is forced to flee (Orange), falls in the middle-ground.  We see a sharper and earlier increase in PPS than the non-sack plays, demonstrating that the pocket is collapsing.  However, the pocket does not collapse as fast as the in-pocket sack, giving the QB time to escape the on-coming rushers. 

<div style="text-align: center;">
    <img src="https://i.imgur.com/02dm3fp.png">
    </div>

Furthermore, we explored whether the evolution of the score has an impact on the pass completion probability. For that purpose, we generated the following figure, illustrating two distinct PPS profiles for complete and incomplete passes.

<div style="text-align: center;">
    <img src="https://i.imgur.com/Vc5ZhUI.png">
    </div>
    
After extracting the maximum PPS from the time series (as specified in _Our Approach_), we establish a correlation between a play's PPS and 4 relevant outcomes:
- Have the offensive linemen failed in their role of protecting the QB? (by which we mean a sack or QB-escape)
- Was the pass complete?
- Was the QB sacked?
- Did the QB stay inside the pocket?

The following figure provides the analysis results, where we can determine by visual inspection that the proposed PPS is highly correlated with the play outcome.  


The differences are clearly visible from the violin plots, but we also ran two-way t-tests to confirm the statistical power of the results, all yielding P<0.05.  For all the "good" offensive line outcomes (Green), we can see that the PPS distributions are much lower than the "bad" outcomes.

<div style="text-align: center;">
<img src="https://i.imgur.com/NbVOuCD.png"
width="800px" height="800px">
    </div>

## 2. Game Analysis
To further understand this metric's influence on a complete game, we average the PPS of all available plays in a given game and correlate it with relevant game outcomes: 
- % Offensive Linemen Failure
- % Pass Completion
- Game Score
- Game Result

This analysis provides a clear correlation between the proposed PPS and % Offensive Linemen Failure and % Pass Completion. Furthermore, despite Game Score and Game Result being a multifactorial outcome, this result indicates that a better PPS enhances the team's chance to score more points and ultimately win the game.

<div style="text-align: center;">
    <img src="https://i.imgur.com/wzRORo1.png"
width="800px" height="800px">
</div>

## 3. Season Analysis
Any team can have a good play or even a good game, but both coaches and fans want to understand whether an offensive linemen unit delivers consistent performance throughout a season. For this purpose, we analysed the results at the season level, unravelling whether the proposed PPS correlates with a good performance throughout the entire season. Firstly, we look at % Offensive Linemen Failure, % Pass Completion and both the cumulative and average Game Score throughout the season, as illustrated in the following figure.

This figure confirms the negative correlation between the PPS and the season performance, with a correlation between PPS, pass completion and score performance. Furthermore, this metric allows further analysis of outliers, such as the Eagles, who have a high PPS while still having above average points-per-game. 

<div style="text-align: center;">
    <img src="https://i.imgur.com/HaRszNM.png"
width="800px" height="800px">
</div>

As a final analysis, we looked at the overall performance across the season in terms of number of wins, as follows:

<div style="text-align: center;">
    <img src="https://i.imgur.com/SAp7DoL.png"
width="500px" height="500px">
</div>

From this analysis, it is clear that consistent linemen performance is required to achieve good results throughout the season, and that the proposed PPS represents and tracks this performance in both individual plays, matches and the entire season. We expect this metric to help coaches and fans identify the teams strengths and weaknesses, empowering them to improve their game over time and taking the NFL to the next level.

# Conclusion and Future Direction
The proposed Pocket Penetration Score (PPS) is a metric that enables the holistic analysis of the offensive linemen unit play. We have provided a framework that isolates line play from all other events that occur during a football play, and demonstrated that this metric correlates with the offensive linemen's performance, which in turn has implications on the team's overall performance and the results achieved.

## Defensive Analysis
The entirety of this analysis has taken the perspective of the offensive line. However, the metric could just as easily be used to evaluate the effect of defensive linemen on a given play or across a season. 

## Individual Player Contribution
One area where this metric could be used is to conduct analysis on the effect that an individual player has on their team's score by comparing plays with/without that player. It could also be used to evaluate the relative importance of a blind-side tackle over the right-side tackle, for instance. 

## Further PPS Time Series Analysis
So far, we have only considered the maximum value during the time series as the PPS. However, we believe the time series generated during the calculation has the potential to provide further insights into the linemen's performance. For instance, the slope of the PPS curve may provide additional insights into the Quarterback's decision process.

# Authors
[Miguel Cacho Soblechero](https://www.linkedin.com/in/miguelcs/)

[Bryce Turner](https://www.linkedin.com/in/brycecturner/)
