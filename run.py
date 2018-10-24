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
def run_agent(join_token):
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

    # As this is a two agent scenario,there will two join tokens
    assert len(join_tokens) == 2
    
    # Run agent-0 on a separate thread
    thread_handler_0, _ = run_agent(join_tokens[0])
    # Run agent-1 on a separate thread
    thread_handler_1, _ = run_agent(join_tokens[1])
    
    # Wait for both the threads to complete execution
    thread_handler_0.join()
    thread_handler_1.join()
    
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
