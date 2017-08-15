module Tags.View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)


view : Model -> Html Msg
view model =
    div [ class "overflow-hidden ph4 ph3-m ph3-l mt5" ]
        [ div [ class "tl w-60-ns center" ] [ h3 [] [ text "Personalise Your Results" ] ]
        , div [ class ("tag-container w-200 relative center " ++ (getPosition model.position)) ]
            [ render_filter_block 1 model.issue_label model.issue_tags model.selected_tags ("mr-5 " ++ (get_active model 1))
            , render_filter_block 2 model.reason_label model.reason_tags model.selected_tags ("mr-5 " ++ (get_active model 2))
            , render_filter_block 3 model.content_label model.content_tags model.selected_tags (get_active model 3)
            ]
        ]


render_filter_block : Int -> String -> List String -> List Tag -> String -> Html Msg
render_filter_block num filter_label tags selected_tags classname =
    div [ class ("br1 shadow-2 w-30 tl pa3 mb3 dib h6 v-mid relative " ++ classname) ]
        ([ h3 [ class "ma0" ] [ text ("Q" ++ (toString num) ++ " of 3") ]
         , h4 [ class "w-70 mv3" ] [ text filter_label ]
         ]
            ++ [ div [ class "pv2" ] ([] ++ (List.map (\t -> render_tag_list t selected_tags num) tags)) ]
            ++ [ div [ class "mt3 absolute bottom-1 w-100 ph3 left-0" ]
                    [ div [ class "w-50 dib tl" ]
                        [ button
                            [ class
                                ("tl dib bn bg-white pointer "
                                    ++ (if num == 1 then
                                            "inactive"
                                        else
                                            ""
                                       )
                                )
                            , onClick (ChangePosition (num - 1))
                            ]
                            [ div [ class "h2 br-100 w2 ba bw2 b--lm-dark-blue lm-orange pa1 mr2 dib" ] [ text "◀" ]
                            , div [ class "dib nunito-bold" ] [ text "previous question" ]
                            ]
                        ]
                    , div [ class "w-50 dib tr" ]
                        [ button
                            [ class
                                ("tr dib bn bg-white pointer "
                                    ++ (if num == 3 then
                                            "inactive"
                                        else
                                            ""
                                       )
                                )
                            , onClick (ChangePosition (num + 1))
                            ]
                            [ div [ class "dib nunito-bold" ] [ text "next question" ]
                            , div [ class "h2 br-100 w2 ba bw2 b--lm-dark-blue lm-orange pa1 ml2 dib" ] [ text "▶" ]
                            ]
                        ]
                    ]
               ]
        )


render_tag_list : String -> List Tag -> Int -> Html Msg
render_tag_list tag selected_tags num =
    div [ class "dib" ]
        [ button
            [ class ("b--lm-orange ba br2 ph2 pv1 lh-tag dib mb1 pointer font nunito " ++ (getTagColour (create_tag num tag) selected_tags))
            , onClick (SelectTag (create_tag num tag))
            ]
            [ text tag ]
        ]


getPosition : Int -> String
getPosition pos =
    case pos of
        1 ->
            "l-20"

        2 ->
            "r-50"

        3 ->
            "r-120"

        _ ->
            "l-20"


getTagColour : Tag -> List Tag -> String
getTagColour tag selected_tags =
    if List.member tag selected_tags then
        "lm-bg-orange-70"
    else
        "lm-bg-orange-20"


create_tag : Int -> String -> Tag
create_tag num name =
    case num of
        1 ->
            Tag "issue" name

        2 ->
            Tag "reason" name

        3 ->
            Tag "content" name

        _ ->
            Tag "issue" name


get_active : Model -> Int -> String
get_active model pos =
    if not (model.position == pos) then
        "inactive"
    else
        ""
