(**** TEST PARAMETRAGE VALIDE ****)

Lgtmaj:=LENGTH_ARW(Tab_maj);	(* Calcul de la longueur de la table de MAJ *)

IF(*1*)
  Tattcal>0 AND +		(*Temps d'attente calculateur >0 *)
  Lgtmaj>0 AND				(* Longueur table de mise à jour >0 *)
  Mfctano>0 AND			(* Mot de fonctionnement en cas d'anomalies >0 *)
  Mfctano<4 AND			(* Mot de fonctionnement en cas d'anomalies <4 *)
  LENGTH_ARW(Tab_ech)=Lgtmaj+4 AND	(* Verification de la longueur de la table d'échange *)
  LENGTH_ARW(Tab_acq)=Lgtmaj		(* Verification de la longueur de la table d'acquisition *)
THEN(*1*)
  
  RESET Dfpara;			(* RAZ Défaut paramétrage *)

  Advalcal:=Lgtmaj+2;		(* Calcul adresse VAL CAL *)
  Admlocal:=Advalcal+1;		(* Calcul adresse MODE LOCAL *)
  
  Valapi :=Tab_ech[0];		(* Calcul valeur VAL API *)
  Valcal :=Tab_ech[Advalcal];	(* Calcul valeur VAL CAL *)
  
    
  (**** ATTENTE REPONSE CALCULATEUR ****)
  
  IF(*2*)
    (Valapi=1 OR
     Valapi=3) AND 
    Valcal=0 AND
    NOT Timeout		(* Pas de Défaut réponse calculateur *)
  THEN(*2*)
    SET Bittempo;	 	(* Lancement temporisation d'attente réponse calculateur *)
  END_IF(*2*);
  
  FTON(Bittempo,Tattcal,Dftempo,Tempo,Dwtempo);  (* Temporisation d'attente calculateur *)

  
  (**** DEPASSEMENT DU TEMPS D'ATTENTE REPONSE CALCULATEUR ****)
  
  IF(*3*)
    Dftempo AND		(* Défaut réponse calculateur *)
    Bittempo			(* Validation temporisation d'attente calculateur *)
  THEN(*3*)
    RESET Bittempo; 	(* Arrêt temporisation d'attente réponse calculateur *)
    SET Timeout;		(* Miseà 1 Défaut réponse calculateur *)
    INC Cptimout;		(* Incrémentation Compteur Time Out calculateur *)
  END_IF(*3*);
  
  
  (**** LE CALCULATEUR A REPONDU A L'AUTOMATE ****)
  
  IF(*4*)
    Valapi=0 AND
    (Valcal=1 OR
  	Valcal=2 OR
  	Valcal=4)
  THEN(*4*)
  
    SET Rep_cal;		(* Mise à 1 Réponse calculateur *)
    RESET Bittempo; 	(* Arrêt temporisation d'attente réponse calculateur *)
    RESET Timeout;		(* RAZ Défaut réponse calculateur *)
  
  ELSE(*4*)
    
    RESET Rep_cal;		(* Mise à 1 Réponse calculateur *)
  
  END_IF(*4*);
  
  
  (**** FIN DU MODE DE FORCAGE ****)
  
  IF(*5*)
    (FE Smf AND		(* Front descendant Sélecteur sur marche forcée *)
     Memforce AND		(* Mémorisation marche forcée *) 
     (NOT Timeout OR	(* Pas de time-out *)
      NOT Autmdeg)) OR	(* Pas d'autorisation de marche dégradée *)
    
    (FE Timeout AND		(* Front descendant time-out *)
     Autmdeg) 			(* Autorisation de marche dégradée *)
  THEN(*5*)
   
    SET Fin_forc;		(* Mise à 1 Fin du mode de forçage *)
    
  END_IF(*5*);  
  
 
  (**** MODE LOCAL = 0 ****)
  
  IF(*6*)
     NOT Smf AND		(* Pas de Sélecteur sur marche forcée *)
     (NOT Timeout OR	(* Pas de time-out *)
      NOT Autmdeg) 		(* Pas d'autorisation de marche dégradée *)
  THEN(*6*)
  
    Tab_ech[Admlocal]:=0;(* Mode local = 0 *)
 
  END_IF;(*6*)   
 
  
  (**** MEMORISATION MODE DE MARCHE FORCEE 
        QUAND LE CALCULATEUR NE REPOND PAS OU
        QUE LES DONNEES SONT INCORRECTES ****)
  
  IF(*7*)
    (Timeout AND		(* Time-out : pas de réponse calculateur *)
     (Autmdeg OR		(* Autorisation de marche dégradée *)
      Smf))			(* Sélecteur sur marche forcée *)
    OR
    (Smf AND  			(* Sélecteur sur marche forcée *)
     (Dfcarinc OR		(* RAZ Défaut caractéristiques incorrectes *)
      Valapi=2 OR
      Valapi=4 OR
      Valapi=5))
  THEN(*7*)
  
    SET Memforce; 		(* Mise à 1 Mémorisation marche forcée *)
    Tab_ech[Admlocal]:=1;(* Mode local =1 *)
  
  END_IF;(*7*) 
 
 
  (**** COMPTEUR DEFAUT CARACTERISTIQUES INCORRECTES ****)
  
  IF(*8*)
    Valcal=4 OR
    Valapi=5
  THEN(*8*)
    
    SET Valcal4;		(* Mise à 1 Valcal4 *)
    
    IF(*9*)
      RE Valcal4		(* Front montant Valcal4 *)
    THEN(*9*)  
      SET Dfcarinc;		(* Mise à 1 Défaut caractéristiques incorrectes *)
      INC Cptdfcar;		(* Incrémentation Compteur caractéristiques incorrectes *)
    END_IF;(*9*)
      
  ELSIF(*8*)
    (Valcal<>4 AND
     Valapi<>5) OR
    (Valcal=4 AND 
     Mfctano=1 AND		(* Pas d'information de la correction au calculateur *)
     RE Fcorrop)		(* Front montant Fin de correction opérateur *)
  THEN(*8*)  
    
    RESET Valcal4;		(* RAZ Valcal4 *)
    RESET Dfcarinc;		(* RAZ Défaut caractéristiques incorrectes *)
    
  END_IF(*8*);
  
    
  (**** TRANSFERT TABLE DE MISE A JOUR VERS BLOC D'ECHANGE ****)
  
  IF(*10*)
    Valapi=0 AND
    (
     ((Valcal=1 OR
       Valcal=4) AND
      RE Demdial)		(* Front montant Demande de dialogue *)
     OR 
     (Valcal=4 AND		(* Anomalies détéctées par calculateur *)
      Mfctano=2 AND		(* Information de la correction au calculateur *)
      RE Fcorrop)		(* Front montant Fin de correction opérateur *)
    )  
  THEN(*10*)
    
    FOR Indmbech:=1 TO Lgtmaj (* Transtert table de mise à jour *)
    DO					(* vers le bloc d'échange *)
      Indmtmaj:=Indmbech-1;
      Tab_ech[Indmbech]:=Tab_maj[Indmtmaj];
    END_FOR;
    
        
    (**** VAL API = 1 ****)
    
    IF(*11*)
      NOT Smf AND			(* Pas de Sélécteur sur marche forcée *)
      (NOT Autmdeg OR		(* Pas d'autorisation de marche dégradée *)
       NOT Timeout) AND		(* Pas de Time-out : le calculateur a répondu dans le délais *)
      NOT Fin_forc			(* Pas de fin du mode de forçage *)
    THEN(*11*)
    
      Valapi:=1;	   		(* VAL API = 1 *)
      Valcal:=0;	  		(* VAL CAL = 0 *)
          
    END_IF;(*11*)
     
    
    (**** VAL API = 3 ****)
        
    IF(*12*)
      Smf OR				(* Sélecteur sur marche forcée *)
      (Autmdeg AND			(* Autorisation de marche dégradée *)
       Timeout) OR			(* Time-out : pas de réponse du calculateur *)
      Fin_forc				(* Fin du mode de forçage *)
    THEN(*12*)
      
      Valapi:=3;			(* VAL API = 3 *)
      Valcal:=0;	  		(* VAL CAL = 0 *)
      
      IF(*13*)
        Fin_forc			(* Fin du mode de forçage *)
      THEN(*13*)  
      
        RESET Fin_forc;		(* RAZ Fin du mode de forçage *)		
        RESET Memforce;		(* RAZ Mémorisation marche forcée *)
      
      ELSE(*13*)
      
        Tab_ech[Admlocal]:=1;	(* Mode local = 1 *)
        SET Memforce;		(* Mise à 1 Mémorisation marche forcée *)
      
      END_IF;(*13*)  
    
    END_IF(*12*);
    
    
    (**** VAL API = 4 ****)
    
    IF(*14*)
      Dfident AND 		(* Défaut identifiant du point d'échange *)
      Valapi<>3
    THEN(*14*)
    
      Valapi:=4;    	(* Anomalie détectée par automate => VAL API = 4 *)
      Valcal:=0;	  	(* VAL CAL = 0 *)
      
    END_IF(*14*);
            
  ELSE(*10*)
  
  
    (**** GESTION MARCHE AVEC ATTENTE DU CALCULATEUR ****)
  
    IF(*15*)
      Demdial AND		(* Demande de dialogue *)
      Valapi=0 AND
      Valcal=2 AND
      NOT Memforce		(* PAS de Mémorisation marche forcée *)
    THEN(*15*)
      
      Valapi:=2;		(* VAL API = 2 *)
      Valcal:=0; 	    	(* VAL CAL = 0 *)
          
    ELSE(*15*)
    
    
      (**** DOUBLE DIALOGUE EN CAS D'ANOMALIES ****)
      
      IF(*16*)
        Demdial AND		(* Demande de dialogue *)
        Valapi=0 AND
        Valcal=4 AND
        Mfctano =3		(* Double dialogue autorisé en cas d'anomalies *)
      THEN(*16*)
      
        Valapi:=5;		(* VAL API = 5 *)
        Valcal:=0;      	(* VAL CAL = 0 *)
                
      END_IF(*16*);
    END_IF(*15*);
  END_IF(*10*);         
  
  Tab_ech[Advalcal]:=Valcal;	(* Copie VAL CAL dans la table d'échange *)
  Tab_ech[0]:=Valapi;		(* Copie VAL API dans la table d'échange *)
 
   
  (**** RECOPIE DES DONNEES DU BLOC D'ECHANGE VERS LA TABLE D'ACQUISITION ****)
  
  IF(*17*)
    Valapi=0 AND
    Valcal=1 AND
    RE Rep_cal			(* Front montant Réponse calculateur *)
  THEN(*17*) 
   
    FOR Indmbech:=1 TO Lgtmaj
    DO
      Indmtmaj:=Indmbech-1;
      Tab_acq[Indmtmaj]:=Tab_ech[Indmbech];
    END_FOR;
  
  END_IF;(*17*)
  
  
  (**** RECOPIE DES DONNEES DE LA TABLE DE MISE A JOUR
        VERS LA TABLE D'ACQUISITION ****)
  
  IF(*18*)
    Valapi=0 AND
    Valcal=4 AND
    Mfctano=1 AND		(* Pas d'information de la correction au calculateur *)
    RE Fcorrop 		(* Front montant Fin de correction opérateur *)  
  THEN(*18*) 
       
    FOR Indmtmaj:=0 TO Lgtmaj-1
    DO
      Tab_acq[Indmtmaj]:=Tab_maj[Indmtmaj];
    END_FOR;
    
    RESET Dfcarinc;		(* RAZ Défaut caractéristiques incorrectes *)
    
  END_IF(*18*);
  
  
  (**** FIN DE L'ECHANGE ****)
  
  IF(*19*)
    Valapi=0 AND
    (
     ((Valcal=1 OR
       Valcal=4) AND   
       RE Rep_cal)		(* Front montant Réponse calculateur *)
     OR 
     (Valcal=4 AND
      Mfctano=1 AND		(* Pas d'information de la correction au calculateur *)
      RE Fcorrop) 		(* Front montant Fin de correction opérateur *)  
    )
  THEN(*19*)
    
    SET Findial;		(* Mise à 1 Fin de dialogue *)
    
  ELSIF(*19*)
    NOT Demdial AND		(* Pas de Demande de dialogue *)
    Findial			(* Fin de dialogue *)
  THEN(*19*)
  
    RESET Findial;		(* RAZ Fin de dialogue *)
      
  END_IF(*19*);
  
    
  (**** RAZ COMPTEURS DEFAUTS ****)
  
  IF(*20*)
    RE Razcmpt			(* Entrée RAZ compteurs de défauts *)
  THEN(*20*)
    Cptimout:=0;		(* RAZ Compteur Time Out calculateur *)
    Cptdfcar:=0;		(* RAZ Compteur défaut caractéristiques incorrectes *)
  END_IF(*20*);


  (**** MISE A JOUR DU MOT DE DIALOGUE ****)
  
  IF(*21*)
    Valcal = 0
  THEN(*21*)
  
    IF(*22*)
      Valapi=1
    THEN(*22*)
      Etatdial := 1;
    END_IF;(*22*)
    
    IF(*23*)
      Valapi=2
    THEN(*23*)
      Etatdial:=2;
    END_IF;(*23*)
    
    IF(*24*)
      Valapi=3
    THEN(*24*)
      Etatdial:=3;
    END_IF;(*24*)
    
    IF(*25*)
      Valapi=4
    THEN(*25*)
      Etatdial:=4;
    END_IF;(*25*)
    
    IF(*26*)
      Valapi=5
    THEN(*26*)
      Etatdial:=5;
    END_IF;(*26*)
          
  END_IF;(*21*)

  IF(*27*)
    Valapi=0
  THEN
    
    IF(*28*)
      Valcal=1
    THEN(*28*)
      Etatdial:=6;
    END_IF;(*28*)
    
    IF(*29*)
      Valcal=2
    THEN(*29*)
      Etatdial:=7;
    END_IF;(*29*)
    
    IF(*30*)
      Valcal=4
    THEN(*30*)
      Etatdial:=8;
    END_IF;(*30*)
        
  END_IF;(*27*)
  
  IF(*31*)
    Valapi=0 AND
    Valcal=0
  THEN(*31*)
    Etatdial:=10;
  ELSIF
    Valapi>5 OR
    Valcal>5 OR
    (Valapi>0 AND
     Valcal>0) 
  THEN(*31*)
    Etatdial:=11;
  END_IF;(*31*)

ELSE(*1*)
  SET Dfpara;		(* Mise à 1 Défaut paramétrage *)
END_IF(*1*);
