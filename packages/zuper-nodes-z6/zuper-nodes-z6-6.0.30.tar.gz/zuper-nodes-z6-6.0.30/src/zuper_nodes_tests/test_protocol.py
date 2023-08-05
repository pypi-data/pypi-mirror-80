import os
from typing import Sequence, List, Union

from networkx.drawing.nx_pydot import write_dot

from zuper_commons.fs import make_sure_dir_exists
from zuper_nodes import OutputProduced, InputReceived, Event, Language, logger, ChannelName

from zuper_nodes.language_parse import parse_language, language_to_str
from zuper_nodes.language_recognize import LanguageChecker, Enough, Unexpected, NeedMore

from comptests import comptest, run_module_tests, get_comptests_output_dir
from zuper_nodes_wrapper.meta_protocol import basic_protocol


def assert_seq(s: Union[str, Language], seq: List[Event], expect: Sequence[type], final: type):
    if isinstance(s, str):
        s = s.replace("\n", " ").strip()
        while "  " in s:
            s = s.replace("  ", " ")
        l = parse_language(s)
    else:
        l = s

    s2 = language_to_str(l)
    print(s)
    print(s2)
    l2 = parse_language(s2)
    assert l == l2, (s, s2)

    pc = LanguageChecker(l)
    logger.info(f"Active start: {pc.get_active_states_names()}")

    dn = get_comptests_output_dir()
    fn = os.path.join(dn, "language.dot")
    make_sure_dir_exists(fn)
    write_dot(pc.g, fn)
    logger.info(f"Written to {fn}")

    # all except last
    for i, (e, r) in enumerate(zip(seq, expect)):
        logger.info(f"Active before: {pc.get_active_states_names()}")
        logger.info(f"Event {e}")
        res = pc.push(e)
        logger.info(f"Active after: {pc.get_active_states_names()}")
        if not isinstance(res, r):
            msg = f"Input {i} ({e}) response was {type(res).__name__} instead of {r.__name__}"
            msg += f"\n entire sequence: {seq}"
            msg += f"\n language: {l}"
            msg += f"\n language string: {s2}"
            raise Exception(msg)

    res = pc.finish()
    if not isinstance(res, final):
        msg = f"finish response was {type(res).__name__} instead of {final.__name__}"
        msg += f"\n entire sequence: {seq}"
        msg += f"\n language: {l}"
        msg += f"\n language string: {s2}"
        raise Exception(msg)


@comptest
def test_proto_out1():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("out:a", seq, (Enough,), Enough)


@comptest
def test_proto_in1():
    seq = [InputReceived(ChannelName("a"))]
    assert_seq("in:a", seq, (Enough,), Enough)


@comptest
def test_proto3():
    seq = [InputReceived(ChannelName("a"))]
    assert_seq("out:a", seq, (Unexpected,), Unexpected)


@comptest
def test_proto4():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("in:a", seq, (Unexpected,), Unexpected)


@comptest
def test_proto05():
    seq = [InputReceived(ChannelName("b"))]
    assert_seq("in:a", seq, (Unexpected,), Unexpected)


@comptest
def test_proto06():
    seq = [OutputProduced(ChannelName("b"))]
    assert_seq("in:a", seq, (Unexpected,), Unexpected)


@comptest
def test_proto07():
    seq = [OutputProduced(ChannelName("a")), OutputProduced(ChannelName("b"))]
    assert_seq("out:a ; out:b", seq, (NeedMore, Enough), Enough)


@comptest
def test_proto08():
    seq = [OutputProduced(ChannelName("a")), OutputProduced(ChannelName("b"))]
    assert_seq("out:a ; out:b ; out:b", seq, (NeedMore, NeedMore), NeedMore)


@comptest
def test_proto09():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("out:a ; out:b", seq, (NeedMore,), NeedMore)


@comptest
def test_proto10():
    seq = [
        OutputProduced(ChannelName("a")),
        OutputProduced(ChannelName("b")),
        OutputProduced(ChannelName("c")),
    ]
    assert_seq("out:a ; out:b", seq, (NeedMore, Enough, Unexpected), Unexpected)


@comptest
def test_proto_zom_01():
    seq = []
    assert_seq("out:a *", seq, (), Enough)


@comptest
def test_proto_zom_02():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("out:a *", seq, (Enough,), Enough)


@comptest
def test_proto_zom_03():
    seq = [OutputProduced(ChannelName("a")), OutputProduced(ChannelName("a"))]
    assert_seq("out:a *", seq, (Enough, Enough), Enough)


@comptest
def test_proto_either_01():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("out:a | out:b ", seq, (Enough,), Enough)


@comptest
def test_proto_either_02():
    seq = [OutputProduced(ChannelName("b"))]
    assert_seq("out:a | out:b ", seq, (Enough,), Enough)


@comptest
def test_proto_either_03():
    seq = [OutputProduced(ChannelName("c"))]
    assert_seq("out:a | out:b | out:c ", seq, (Enough,), Enough)


@comptest
def test_proto_either_04():
    seq = [OutputProduced(ChannelName("a")), OutputProduced(ChannelName("b"))]
    assert_seq("(out:a ; out:b) | (out:b ; out:a) ", seq, (NeedMore, Enough), Enough)


@comptest
def test_proto_either_05():
    seq = [OutputProduced(ChannelName("b")), OutputProduced(ChannelName("a"))]
    assert_seq("(out:a ; out:b) | (out:b ; out:a) ", seq, (NeedMore, Enough,), Enough)


@comptest
def test_proto_oom_01():
    seq = []
    assert_seq("out:a +", seq, (), NeedMore)


@comptest
def test_proto_oom_02():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("out:a +", seq, (Enough,), Enough)


@comptest
def test_proto_oom_03():
    seq = [OutputProduced(ChannelName("a")), OutputProduced(ChannelName("a"))]
    assert_seq("out:a +", seq, (Enough, Enough), Enough)


@comptest
def test_proto_zoom_01():
    seq = []
    assert_seq("out:a ?", seq, (), Enough)


@comptest
def test_proto_zoom_02():
    seq = [OutputProduced(ChannelName("a"))]
    assert_seq("out:a ?", seq, (Enough,), Enough)


@comptest
def test_proto_zoom_03():
    seq = [OutputProduced(ChannelName("a")), OutputProduced(ChannelName("a"))]
    assert_seq("out:a ?", seq, (Enough, Unexpected), Unexpected)


@comptest
def test_protocol_complex1():
    l = """
        (
            in:next_episode ; (
                out:no_more_episodes | 
                (out:episode_start ;
                    (in:next_image ; (out:image | out:no_more_images))*)
            )
        )*            
    """
    seq = [InputReceived(ChannelName("next_episode")), OutputProduced(ChannelName("episode_start"))]
    assert_seq(l, seq, (NeedMore, Enough), Enough)


@comptest
def test_protocol_complex1_0():
    l = """
        
            in:next_episode ; (
                out:no_more_episodes | 
                (out:episode_start ;
                    (in:next_image ; (out:image | out:no_more_images))*)
            )
                    
    """
    seq = [InputReceived(ChannelName("next_episode")), OutputProduced(ChannelName("no_more_episodes"))]
    assert_seq(l, seq, (NeedMore, Enough), Enough)


@comptest
def test_protocol_complex1_1():
    l = """

               in:next_episode ; (
                   out:no_more_episodes | 
                   (out:episode_start ;
                       (in:next_image ; (out:image | out:no_more_images))*)
               )

       """
    seq = [InputReceived(ChannelName("next_episode")), OutputProduced(ChannelName("episode_start"))]
    assert_seq(l, seq, (NeedMore, Enough), Enough)


@comptest
def test_protocol_complex1_2():
    l = """

               in:next_episode ; (
                   out:no_more_episodes | 
                   (out:episode_start ;
                       (in:next_image ; (out:image | out:no_more_images))*)
               )

       """
    seq = [
        InputReceived(ChannelName("next_episode")),
        OutputProduced(ChannelName("episode_start")),
        InputReceived(ChannelName("next_image")),
        OutputProduced(ChannelName("image")),
    ]
    assert_seq(l, seq, (NeedMore, Enough), Enough)


@comptest
def test_protocol_complex1_3():
    l = """
                (
                    in:next_episode ; (
                        out:no_more_episodes | 
                        (out:episode_start ;
                            (in:next_image ; (out:image | out:no_more_images))*)
                    )
                )*            
            """
    seq = [
        InputReceived(ChannelName("next_image")),
    ]
    assert_seq(l, seq, (Unexpected,), Unexpected)


@comptest
def test_protocol_complex1_3b():
    l = """
                (
                    in:next_episode ; (
                        out:no_more_episodes | 
                        (out:episode_start ;
                            (in:next_image ; (out:image | out:no_more_images))*)
                    )
                )*            
            """
    seq = [
        InputReceived(ChannelName("next_image")),
    ]
    assert_seq(l, seq, (Unexpected,), Unexpected)


@comptest
def test_protocol_complex1_3c():
    l = """
                (
                    in:next_episode ; (
                         
                        (out:episode_start ;
                            (in:next_image)*)
                    )
                )*            
            """
    seq = [
        InputReceived(ChannelName("next_image")),
    ]
    assert_seq(l, seq, (Unexpected,), Unexpected)


@comptest
def test_protocol_complex1_3e():
    l = """
                (
                    in:next_episode ; (

                        (out:episode_start ;
                            (in:next_image)*)
                    )
                )         
            """
    seq = [
        InputReceived(ChannelName("next_image")),
    ]
    assert_seq(l, seq, (Unexpected,), Unexpected)


@comptest
def test_protocol_complex1_3d():
    l = """
                (
                    in:next_episode ; (

                        (out:episode_start ;
                            (in:next_image))
                    )
                )*            
            """
    seq = [
        InputReceived(ChannelName("next_image")),
    ]
    assert_seq(l, seq, (Unexpected,), Unexpected)


@comptest
def test_protocol_complex1_3v():
    l0 = """

        out:episode_start ;
            (in:next_image ; (out:image | out:no_more_images))*

        """
    seq = [OutputProduced(ChannelName("episode_start"))]
    assert_seq(l0, seq, (Enough,), Enough)


@comptest
def test_basic_protocol1():
    l0 = basic_protocol.language
    seq = [InputReceived(ChannelName("set_config"))]
    assert_seq(l0, seq, (NeedMore,), NeedMore)


if __name__ == "__main__":
    run_module_tests()
