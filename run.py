import marlo
import os
import json


def get_join_tokens():
    if marlo.is_grading():
        """
            In the crowdAI Evaluation environment obtain the join_tokens 
            from the evaluator
            
            the `params` parameter passed to the `evaluator_join_token` only allows
            the following keys : 
                    "seed",
                    "tick_length",
                    "max_retries",
                    "retry_sleep",
                    "step_sleep",
                    "skip_steps",
                    "videoResolution",
                    "continuous_to_discrete",
                    "allowContinuousMovement",
                    "allowDiscreteMovement",
                    "allowAbsoluteMovement",
                    "add_noop_command",
                    "comp_all_commands"
                    # TODO: Add this to the official documentation ? 
                    # Help Wanted :D Pull Requests welcome :D 
        """
        join_tokens = marlo.evaluator_join_token(params={})

    else:
        """
            When debugging locally,
            Please ensure that you have a Minecraft client running on port 10000 and 10001
            by doing : 
            $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10000
            $MALMO_MINECRAFT_ROOT/launchClient.sh -port 10001
        """
        print("Generating join tokens locally...")
        client_pool = [('127.0.0.1', 10000), ('127.0.0.1', 10001)]
        join_tokens = marlo.make('MarLo-BuildbattleTrain1-v0',
                                 params={
                                    "client_pool": client_pool,
                                    "agent_names" : [
                                        "MarLo-Agent-0",
                                        "MarLo-Agent-1"
                                    ]
                                 })
    return join_tokens

@marlo.threaded
def run_agent(join_token, agent_id):
    """
        Where agent_id is an integral number starting from 0
        In case, you have requested GPUs, then the agent_id will match 
        the GPU device id assigneed to this agent.
    """
    env = marlo.init(join_token)
    observation = env.reset()
    done = False
    count = 0
    while not done:
        _action = env.action_space.sample()
        obs, reward, done, info = env.step(_action)
        print("reward:", reward)
        print("done:", done)
        print("info", info)
    
    # It is important to do this env.close()   
    env.close()

def run_episode():
    """
    Single episode run
    """
    join_tokens = get_join_tokens()
    
    # When the required number of episodes are evaluated
    # The evaluator returns False for join_tokens
    if not join_tokens:
        return
        
    thread_handlers = []
    
    """
    NOTE: If instead of a dynamic loop, you hard code the run_agent 
    function calls, then the evaluation of your code will fail in case 
    of a tournament, where multiple submissions can control different agents 
    in the same game. 
    """
    for _idx, join_token in enumerate(join_tokens):
        # Run agent-N on a separate thread
        thread_handler, _ = run_agent(join_token, _idx)
        
        # Accumulate thread handlers
        thread_handlers.append(thread_handler)
    
    # Wait for  threads to complete
    for thread_handler in thread_handlers:
        thread_handler.join()    
    
    print("Episode Run Complete")

if __name__ == "__main__":
    """
        In case of debugging locally, run the episode just once
        and in case of when the agent is being evaluated, continue 
        running episodes for as long as the evaluator keeps supplying
        join_tokens.
    """
    if not marlo.is_grading():
        print("Running single episode...")
        run_episode()
    else:
        while True:
            run_episode()
