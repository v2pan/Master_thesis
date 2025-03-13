from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database
from Main.join_pipeline_aux import compare_semantics_in_list
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def tuple_bleu_score(candidate, reference, n_gram=1):
    """
    Compute BLEU score between two tuples treated as sentences.
    n_gram: how many grams to consider for BLEU (1, 2, 3, etc.)
    """
    weights = tuple((1.0 / n_gram for _ in range(n_gram)))  # e.g., (1.0,) for 1-gram, (0.5, 0.5) for 2-gram
    chencherry = SmoothingFunction()
    return sentence_bleu([reference], candidate, weights=weights, smoothing_function=chencherry.method1)

def average_best_bleu_score(answer, required_answer, n_gram=1):
    """
    For each tuple in 'answer', find the best BLEU match in 'required_answer'.
    Return average of these best scores.
    """
    if not answer or not required_answer:
        return 0.0  # No data to compare

    best_scores = []
    for candidate in answer:
        best_score = 0.0
        for reference in required_answer:
            score = tuple_bleu_score(candidate, reference, n_gram=n_gram)
            best_score = max(best_score, score)
        best_scores.append(best_score)

    final_score = sum(best_scores) / len(best_scores)
    return final_score

# Example data
answer = {('apple', 'banana'), ('carrot', 'date')}
required_answer = {('apple', 'date'), ('banana', 'carrot')}
# required_answer = set()

# Calculate final average similarity score
final_similarity_score = average_best_bleu_score(answer, required_answer, n_gram=1)
print(f"Final Similarity Score: {final_similarity_score:.4f}")


# answer, metadata = combined_pipeline(query=None,initial_sql_query="SELECT * FROM right_table JOIN left_table ON left_table.aggregate = right_table.aggregate;",aux=True)
# # order= [['left_table.aggregate', 'right_table.aggregate']]
# # input_list= [[('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('title (deluxe)\nmeghan trainor\n 2014, 2015 epic records, a division of sony music entertainment\n9-Jan-15\ncredit\n2:51',), ('slow down (remixes)\nselena gomez\n 2013 hollywood records, inc.\n20-Aug-13\nslow down (smash mode remix)\n5:21',), ('slow down (reggae remixes) - single\nselena gomez\n 2013 hollywood records, inc.\n20-Aug-13\nslow down (sure shot rockers reggae dub remix)\n3:15',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('the reason - ep\nx ambassadors\n 2015 kidinakorner/interscope records\n10-Aug-15\nshining\n3:40',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('vhs\nx ambassadors\n 2015 kidinakorner/interscope records\n30-Jun-15\nvhs outro (interlude)\n1:25',), ('hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28',), ('hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28',), ('hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28',), ('hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28',), ('hotel cabana\nnaughty boy\n 2014 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nepilogue (feat. george the poet)\n1:28',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('hotel cabana (deluxe version)\nnaughty boy\n 2013 naughty boy recordings ltd under exclusive licence to virgin records ltd\n6-May-14\nlifted (feat. emeli sand\x90© & professor green)\n4:15',), ('get free - single\nmajor lazer\n 2013 secretly canadian / mad decent\n27-Feb-13\nget free (andy c remix)\n5:31',), ('original don (feat. the partysquad) [remixes] - ep\nmajor lazer\n 2011 downtown records unders exclusive license to interscope records in the u.s.a.\n1-Nov-11\noriginal don (feat. the partysquad) [the partysquad & punish smash em remix]\n3:38',), ('peace is the mission\nmajor lazer\n 2015 mad decent\n1-Jun-15\nall my love (feat. ariana grande & machel montano) [remix]\n3:49',), ('original don (feat. the partysquad) [remixes] - ep\nmajor lazer\n 2011 downtown records unders exclusive license to interscope records in the u.s.a.\n1-Nov-11\noriginal don (feat. the partysquad) [the partysquad & punish smash em remix]\n3:38',), ('get free - single\nmajor lazer\n 2013 secretly canadian / mad decent\n27-Feb-13\nget free (andy c remix)\n5:31',), ('nick jonas (deluxe version)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48',), ('nick jonas\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\nnothing would be better\n4:34',), ('nick jonas (deluxe)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48',), ('nick jonas (deluxe)\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\ncloser (feat. mike posner)\n3:48',), ('nick jonas\nnick jonas\n 2014 island records, a division of umg recordings, inc. / safehouse records, llc\n10-Nov-14\nnothing would be better\n4:34',), ('#NAME?\ned sheeran\n 2011 warner music uk limited\n9-Sep-11\nsunburn\n4:35',), ('5\ned sheeran\n 2014 warner music uk limited\n23-Jun-14\ngoodbye to you (feat. dot rotten)\n5:30',), ('loose change\ned sheeran\n 2010 all tracks (p) 2010 paw print records under exclusive license to warner music uk limited except for track 1 (p) 2011paw print records under exclusive license to warner music uk limited\n9-Dec-11\nfirefly (bravado dubstep remix)\n4:29',), ('x\ned sheeran\n 2014 asylum records uk, a warner music uk company\n20-Jun-14\nafire love\n5:14',), ('itunes festival: london 2012 - ep\ned sheeran\n 2012 warner music uk limited\n3-Sep-12\nthe a team (live)\n5:01',)]]
# # compare_semantics_in_list(input_list, order)
# print(answer)