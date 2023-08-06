import torch
from torch import nn
from torch.nn import CrossEntropyLoss
from transformers import BertModel, BertPreTrainedModel


class BertForMRCYesNoNoAns(BertPreTrainedModel):
    def __init__(self, config):
        super(BertForMRCYesNoNoAns, self).__init__(config)
        self.bert = BertModel(config)
        self.qa_outputs = nn.Linear(config.hidden_size, 2)
        self.cls_outputs = nn.Linear(config.hidden_size, 3)
        self.init_weights()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None,
                start_positions=None, end_positions=None, target_labels=None):
        sequence_output, pooled_output = self.bert(input_ids,attention_mask=attention_mask,token_type_ids=token_type_ids)
        logits = self.qa_outputs(sequence_output)
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)
        end_logits = end_logits.squeeze(-1)
        target_logits = self.cls_outputs(pooled_output)

        if start_positions is not None and end_positions is not None:
            # If we are on multi-GPU, split add a dimension
            if len(start_positions.size()) > 1:
                start_positions = start_positions.squeeze(-1)
            if len(end_positions.size()) > 1:
                end_positions = end_positions.squeeze(-1)
            # sometimes the start/end positions are outside our model inputs, we ignore these terms
            ignored_index = start_logits.size(1)
            start_positions.clamp_(0, ignored_index)
            end_positions.clamp_(0, ignored_index)

            loss_fct = CrossEntropyLoss(ignore_index=ignored_index)
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)

            # classifier loss
            loss_fct_cls = CrossEntropyLoss(ignore_index=-1)  # no loss for has answer
            cls_loss = loss_fct_cls(target_logits, target_labels)

            total_loss = ((start_loss + end_loss) / 2) + cls_loss
            return total_loss
        else:
            return start_logits, end_logits, target_logits
