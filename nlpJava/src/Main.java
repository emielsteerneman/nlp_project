import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.realiser.english.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;

public class Main {

    public static void main(String[] args) {
        Lexicon lexicon = Lexicon.getDefaultLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexicon);
        Realiser realiser = new Realiser(lexicon);

        NLGElement s1 = nlgFactory.createSentence("my dog is happy");
        String output = realiser.realiseSentence(s1);
        System.out.println(output);

        NLGElement NP, VP, VP1, PP;
        NP = nlgFactory.createNounPhrase("man");
        ((NPPhraseSpec) NP).setDeterminer("the");
        ((NPPhraseSpec) NP).addPreModifier("drunken");
        ((NPPhraseSpec) NP).addPreModifier("floridian");
        PP = nlgFactory.createPrepositionPhrase("into the store");
        VP = nlgFactory.createVerbPhrase("carrying");
        ((VPPhraseSpec) VP).setObject("alligator");
        VP1 = nlgFactory.createVerbPhrase("remember");
        VP1.setFeature(Feature.NEGATED, true);
        SPhraseSpec p = nlgFactory.createClause();
        p.setSubject(NP);
//        p.setVerb("remember");
//        p.addModifier("can");
        p.setVerbPhrase(VP1);
        p.addComplement(VP);
        p.addComplement(PP);
//        p.setVerbPhrase(VP);
//        SPhraseSpec p1 = nlgFactory.createClause();
//        p1.setSubject(p);
//        p1.setVerb("carrying");
//        p1.setObject("alligator");
//        p1.setObject();

        String output2 = realiser.realiseSentence(p); // Realiser created earlier.
        System.out.println(output2);
    }

}
